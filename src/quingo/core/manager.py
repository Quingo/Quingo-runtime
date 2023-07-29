import platform
import subprocess
import logging
from quingo.core.quingo_task import Quingo_task
from quingo.if_backend.backend_hub import Backend_hub, Backend_info
import quingo.core.data_transfer as dt
from pathlib import Path
from .compiler_config import get_mlir_path
from quingo.core.utils import (
    quingo_err,
    quingo_msg,
    quingo_warning,
    get_logger,
    quingo_info,
)
from quingo.if_backend.qisa import *
from quingo.core.preparation import gen_main_file

logger = get_logger((__name__).split(".")[-1])


class Runtime_system_manager:
    def __init__(self, verbose=False, log_level=logging.WARNING, **kwargs):
        """The quingo runtime system manager.

        Args:
            verbose (bool, optional): If the output message is verbose or not. Defaults to False.
            log_level (level, optional): Logging level. Defaults to logging.WARNING. Allowed values:
              - logging.DEBUG
              - logging.TRACE
              - logging.INFO
              - logging.WARNING
              - logging.ERROR
        """
        self.supported_backend = [
            "pyqcas_quantumsim",
            "cactus_quantumsim",
            "cactus_light_quantumsim",
            "pyqcisim_quantumsim",
            "zuchongzhi",
            "quantify",
        ]

        # define verbose & log_level here which will be used by backends
        self.verbose = verbose
        self.log_level = log_level

        self.config_execution("one_shot", 1)

        self.backend = None  # to be connected
        self.backend_info = None
        if "backend" in kwargs:
            self.set_backend(kwargs["backend"])

        self.set_verbose(verbose)
        self.set_log_level(log_level)

        self.qg_main_fn = None  # pathlib.Path

        self.qasm_file_path = None  # pathlib.Path

        self.qubits_info_path = None  # pathlib.Path

        self.data_block = ""

        # Set to False upon `call_quingo`.
        # After the backend returns successfully, it is set back to True.
        self.success_on_last_execution = False

        self.shared_addr = 0
        self.static_addr = 0x10000
        self.dynamic_addr = 0x20000
        self.max_unroll = 100

        if self.verbose:
            logger.debug("Python version: {}".format(platform.python_version()))

    def set_call_kernel_success(self, success):
        assert isinstance(success, bool)
        if not success:
            self.qasm_file_path = None
        self.success_on_last_execution = success

    def set_log_level(self, log_level):
        self.log_level = log_level
        logger.setLevel(self.log_level)

        backend = self.get_backend()
        if backend is not None:
            backend.set_log_level(log_level)

    def set_verbose(self, v: bool = False):
        """Set the message level to verbose or not.

        Args:
            v (bool): True or False.
        """
        assert isinstance(v, bool)
        self.verbose = v
        backend = self.get_backend()
        if backend is not None:
            backend.set_verbose(v)

    def call_quingo(self, qg_filename: str, qg_func_name: str, *args):
        """This function triggers the main process."""
        self.set_call_kernel_success(False)
        success = self.main_process(qg_filename, qg_func_name, *args)
        self.set_call_kernel_success(success)

        return success

    def set_qubits_info_path(self, qubits_info_path: Path):
        self.qubits_info_path = qubits_info_path.absolute()
        print(self.qubits_info_path)
        if not self.qubits_info_path.exists():
            raise FileNotFoundError(
                "Cannot find the qubits info file: {}".format(self.qubits_info_path)
            )

    def get_last_qasm(self):
        if self.qasm_file_path is None or not self.qasm_file_path.is_file():
            return ""
        with self.qasm_file_path.open("r") as f:
            return f.read()

    def get_last_qasm_file(self):
        if self.qasm_file_path is None or not self.qasm_file_path.is_file():
            return None
        return self.qasm_file_path

    def main_process(self, qg_filename: str, qg_func_name: str, *args):
        """This function is the main function of the manager, which describes the main process:
          1. prepare the hyper() function
          2. compile the Quingo program including the hyper() function
            - different low-level formats can be generated according to the compilation settings
          3. Upload the assembly code or binary code to the backend for execution

        Args:
            qg_filename (str) :  the name of the Quingo file which contains the
                quantum function called by the host program.
            qg_func_name (str) : the name of the quantum function
            args: a variable length of parameters passed to the quantum function
        """

        if not self.compile_process(qg_filename, qg_func_name, *args):
            quingo_err("Compilation failed. Abort.")
            return False

        if not self.execute():  # execute the eQASM file
            quingo_err("Execution failed. Abort.")
            return False

        if self.verbose:
            quingo_msg("Execution finished.")

        # read back the results
        self.result = self.get_backend().read_result()

        return True

    def config_execution(self, mode: str, num_shots: int = 1):
        """Configure the execution mode to 'one_shot' or 'state_vector'.
        When the execution mode is 'one_shot', the number of times to run the uploaded quantum
        circuit can be configured using the parameter `num_shots` at the same time.
        """

        if mode not in ["one_shot", "state_vector"]:
            raise ValueError(
                "Found unrecognized execution mode: '{}'.".format(mode)
                + "Allowed values are: 'one_shot' or 'state_vector'."
            )

        self.mode = mode
        self.num_shots = num_shots

    def set_num_shots(self, num_shots: int):
        """[Deprecated method]. Set the number of times to run the uploaded quantum circuit in
        simulation. In other words, `num_shots` groups of measurement result will be generated.

        Args:
            num_shots (int): The number of times to run the quantum circuit.
        """
        # print("set_num_shots: ", num_shots)
        self.num_shots = num_shots

    #####################################################################
    # Backend related methods
    #####################################################################
    def get_backend(self):
        return self.backend

    def get_backend_info(self) -> Backend_info:
        return self.backend_info

    def set_backend(self, backend_name: str):
        backend_name = backend_name.lower()
        backend_hub = Backend_hub()
        if not backend_hub.support(backend_name):
            logger.error(
                "The chosen backend ({}) is currently not "
                "supported by qgrtsys.".format(backend_name)
            )

            raise ValueError("Undefined backend ({})".format(backend_name))
        self.backend_info = backend_hub.backends[backend_name]

    def get_backend_or_connect_default(self):
        if self.backend is None:
            if self.backend_info is None:
                quingo_info(
                    "No backend has been connected. "
                    "Trying to connect the default PyQCAS backend..."
                )
                # connect to the defacult backend pyqcas_quantumsim
                if not self.connect_backend("pyqcas_quantumsim"):
                    raise SystemError("Cannot connect to the default backend.")
            else:
                if not self.connect_backend(self.get_backend_name()):
                    raise SystemError("Cannot connect to the backend.")
        return self.backend

    def get_backend_info_or_set_default(self) -> Backend_info:
        if self.backend_info is None:
            quingo_info(
                "No backend has been set. "
                "Trying to set the default PyQCAS backend..."
            )
            self.set_backend("pyqcas_quantumsim")
        return self.backend_info

    def get_backend_name(self):
        """return the name of the backend that is being used.
        An empty string will be returned if no backend has been set.
        """
        backend = self.get_backend_info()
        if backend is None:
            return ""
        return "{}".format(backend.module_name)

    def connect_backend(self, backend_name: str):
        """This function set the backend to execute the quantum application.
        Allowed backend includes:
         - 'cactus_quantumsim'
         - 'cactus_light_quantumsim'
         - 'pyqcas_quantumsim'
         - 'pyqcisim_quantumsim': QCIS architecture simulator and QuantumSim qubit state simulator.
         - 'pyqcisim_tequila': QCIS architecture simulator and Tequila tensor simulator.
         - 'zuchongzhi' : to be connected.
        """
        self.set_backend(backend_name)
        if self.backend_info is None:
            quingo_err("No backend has been set.")
            raise SystemError("No backend has been set.")

        backend_name = self.backend_info.module_name
        print("connecting {}...".format(backend_name))

        try:
            self.backend = self.backend_info.get_instance()
        except Exception as e:
            quingo_err(
                "Cannot connect backend '{}' with the following error:".format(
                    backend_name
                )
            )
            quingo_err("{}".format(e))
            quingo_info(
                "To fix this problem, you could explicitly connect another "
                "backend use the the following method: \n"
                "        `quingo_interface.connect_backend(<backend_name>)`\n"
                "    or, install the corresponding simulation backend using:\n"
                "        `pip install pyqcas`\n"
                "    or\n"
                "        `pip install pyqcisim`\n"
                "    or\n"
                "        `pip install symqc`\n"
            )
            return False

        if self.backend is None:
            msg = "Failed to connect the backend: " + backend_name
            quingo_err(msg)
            logger.error(msg)
        else:
            msg = "successfully connected the backend: " + backend_name
            # logger.info(msg)

        self.backend.set_log_level(self.log_level)
        self.backend.set_verbose(self.verbose)
        # print("connect success")
        return True

    def execute(self):
        """This function upload the compiled quantum program, i.e., instruction-format program
        to the backend, and executes it.
        After the execution, the result can be fetched via `read_result()`.
        """
        backend = self.get_backend_or_connect_default()
        if backend.available is False:
            raise EnvironmentError(
                "The backend {} is not available.".format(backend.name())
            )

        if self.mode == "state_vector" and not backend.is_simulator():
            raise ValueError(
                "Cannot retrieve state vector from a non-simulator backend."
            )

        if self.verbose:
            quingo_msg(
                "Uploading the program to the backend {}...".format(backend.name())
            )

        if not backend.upload_program(self.qasm_file_path):
            quingo_err(
                "Failed to upload the program to the backend {}.".format(backend.name())
            )
            quingo_info(
                "  Suggestion: are you uploading QCIS program to an eQASM backend "
                "or eQASM program to a QCIS backend?\n"
                "    If so, please specify the compiler and backend accordingly."
            )
            return False

        if self.verbose:
            quingo_msg("Start execution with {}... ".format(backend.name()))

        if backend.name().lower() in [
            "pyqcisim_quantumsim",
            "pyqcisim_tequila",
            "symqc",
            "zuchongzhi",
        ]:
            return backend.execute(self.mode, self.num_shots)
        else:
            return backend.execute()

    def read_result(self, start_addr):
        if self.success_on_last_execution is False:
            quingo_warning("Last execution fails and no result is read back.")
            return None

        qisa_used = self.get_backend().get_qisa()
        if qisa_used == "eqasm":
            data_trans = dt.Data_transfer()
            data_trans.set_data_block(self.result)
            pydata = data_trans.bin_to_pydata(self.ret_type, start_addr)
            logger.debug("The data converted from the binary is: \n{}\n".format(pydata))
            return pydata

        elif qisa_used == "qcis":
            return self.result

        else:
            raise ValueError(
                "Reading result from a program with unsupported QISA: {}".format(
                    qisa_used
                )
            )
