from logging import log
from quingo.core.manager import *
from quingo.core.data_transfer import *


class If_Quingo():
    def __init__(self, verbose=False, log_level=logging.WARNING, **kwargs):
        self.rsm = Runtime_system_manager(**kwargs)
        self.set_verbose(verbose)
        self.set_log_level(log_level)
        self.data_transfer = Data_transfer()

    def set_verbose(self, v):
        """Set the message level to verbose or not.

        Args:
            v (bool): True or False.
        """
        self.verbose = v
        self.rsm.set_verbose(v)

    def set_log_level(self, log_level):
        self.log_level = log_level
        self.rsm.set_log_level(log_level)

    def connect_backend(self, backend):
        """This function connect the backend to execute quantum applications.
        Allowed backend includes:
         - 'cactus_quantumsim'
         - 'cactus_light_quantumsim'
         - 'pyqcas_quantumsim'
         - 'pyqcisim_quantumsim': QCIS architecture simulator and QuantumSim qubit state simulator.
         - 'zuchongzhi' : to be connected.
        """
        return self.rsm.connect_backend(backend)

    def get_backend_name(self):
        return self.rsm.get_backend_name()

    def set_compiler(self, compiler_name):
        """Set the compiler used to compiler the quingo program.

        Args:
            compiler_name (string): the name of the compiler to use. Default to 'xtext'.
            Allowed values:
              - xtext
              - mlir
        """
        self.rsm.set_compiler(compiler_name)

    def set_eqasm_filename(self, tmp_eqasm_filename):
        self.rsm.set_eqasm_filename(tmp_eqasm_filename)

    def get_last_qasm(self):
        '''Get the qasm code generated by the last execution.
        '''
        return self.rsm.get_last_qasm()

    def config_execution(self, mode: str, num_shots: int = 1):
        '''Configure the execution mode to 'one_shot' or 'state_vector'.
        When the execution mode is 'one_shot', the number of times to run the uploaded quantum
        circuit can be configured using the parameter `num_shots` at the same time.
        '''
        self.rsm.config_execution(mode, num_shots)

    def set_num_shots(self, num_shots: int):
        """Set the number of times to run the uploaded quantum circuit in simulation. In other
           words, `num_shots` groups of measurement result will be generated.

        Args:
            num_shots (int): The number of times to run the quantum circuit.
        """
        self.rsm.set_num_shots(num_shots)

    def call_quingo(self, qg_filename, qg_func_name, *args):
        """This function provides a method in Python to call quantum kernels
        written in Quingo. After the execution of the quantum kernel, the
        result can be read back using the function `read_result`.

        Args:
            qg_filename (str) :  the name of the Qingo file which contains the
                quantum function called by the host program.
            qg_func_name (str) : the name of the quantum function
            args (dict): a variable length of parameters passed to the quantum function
        """
        return self.rsm.call_quingo(qg_filename, qg_func_name, *args)

    def read_result(self, start_addr=0x0):
        """After the execution of the quantum kernel, the result can be read back using
        this function.
        """
        return self.rsm.read_result(start_addr)


if_quingo = If_Quingo()