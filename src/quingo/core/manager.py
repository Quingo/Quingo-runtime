import shutil
from quingo.if_backend.backend_hub import Backend_hub
import quingo.global_config as gc
import quingo.core.data_transfer as dt
import os
import re
import platform
import subprocess
import logging
import distutils.spawn
from pathlib import Path
from quingo.core.utils import quingo_err, quingo_msg, quingo_warning, get_logger, quingo_info
logger = get_logger((__name__).split('.')[-1])


def remove_comment(qu_src):
    search_annotation_string = r'\/\/.*\n'
    return re.sub(search_annotation_string, '', qu_src)


def get_ret_type(qg_filename: str, qg_func_name: str):
    """This function read the Quingo source file to retrieve the return
    type of called Quingo operation.

    Args:
        qg_filename (path) :  the name of the Quingo file which contains the
            quantum function called by the host program.
        qg_func_name (str) : the name of the Quingo function.
    """
    with open(qg_filename, 'r', encoding='utf-8') as qu_src_file:
        qu_src = qu_src_file.read()

    qu_src = remove_comment(qu_src)

    search_string = r'\boperation\b\s+' + \
        qg_func_name + r'\s*\((.*)\)\s*:(.*)\s*\{'

    op_def_components = re.search(search_string, qu_src)
    if op_def_components is None:
        raise ValueError("Cannot find the operation ({}) in the given Quingo source "
                         "file ({}).".format(qg_func_name, qg_filename))

    ret_type = re.sub(r'\d', '', op_def_components.groups()[1].strip())
    return ret_type


class Runtime_system_manager():
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
            compiler (string, optional): which compiler to use. Default to xtext. Allowed values:
              - xtext
              - mlir
        """
        self.supported_compilers = ["xtext", "mlir"]
        # self.compiler_path = {
        #     "xtext": gc.xtext_compiler_path,
        #     "mlir": gc.mlir_compiler_path
        # }
        # self.compiler_name = kwargs.pop('compiler', "xtext")
        # if (self.compiler_name not in self.compiler_path):
        #     raise ValueError(
        #         "Found unsupported compiler: {}".format(self.compiler_name))

        # define verbose & log_level here which will be used by backends
        self.verbose = verbose
        self.log_level = log_level

        self.config_execution('one_shot', 1)

        self.compiler_name = None  # to be set
        self.backend = None  # to be connected

        self.set_verbose(verbose)
        self.set_log_level(log_level)

        self.main_file_fn = None  # pathlib.Path

        self.qasm_file_path = None  # pathlib.Path

        self.data_block = ""

        # Set to False upon `call_quingo`.
        # After the backend returns successfully, it is set back to True.
        self.success_on_last_execution = False

        self.shared_addr = 0
        self.static_addr = 0x10000
        self.dynamic_addr = 0x20000
        self.max_unroll = 100

        if self.verbose:
            logger.debug("Python version: {}".format(
                platform.python_version()))

    def set_call_kernel_success(self, success):
        assert(isinstance(success, bool))
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
        assert(isinstance(v, bool))
        self.verbose = v
        backend = self.get_backend()
        if backend is not None:
            backend.set_verbose(v)

    def get_compiler(self):
        """Get the name of the compiler that has been set.
        If not compiler has been set, return None.
        """
        return self.compiler_name

    def set_compiler(self, compiler_name):
        """Set the compiler used to compiler the quingo program.

        Args:
            compiler_name (string): the name of the compiler to use. Default to 'xtext'.
            Allowed values:
              - xtext
              - mlir
        """
        if (compiler_name not in self.supported_compilers):
            raise ValueError("Found unsupported compiler: {}".format(compiler_name))

        self.compiler_name = compiler_name

    def get_backend(self):
        return self.backend

    def get_backend_or_connect_default(self):
        if self.backend is None:
            quingo_info("No backend has been connected. "
                        "Trying to connect the default PyQCAS backend...")
            if not self.connect_backend('pyqcas_quantumsim'):
                raise SystemError("Cannot connect to the default backend.")
        return self.backend

    def get_backend_name(self):
        backend = self.get_backend()
        if backend is None:
            return ""
        return "{}".format(backend.name())

    def connect_backend(self, backend_name: str):
        """This function set the backend to execute the quantum application.
        Allowed backend includes:
         - 'cactus_quantumsim'
         - 'cactus_light_quantumsim'
         - 'pyqcas_quantumsim'
         - 'pyqcisim_quantumsim': QCIS architecture simulator and QuantumSim qubit state simulator.
         - 'zuchongzhi' : to be connected.
        """

        backend_name = backend_name.lower()
        print("connecting {}...".format(backend_name))

        backend_hub = Backend_hub()
        if not backend_hub.support(backend_name):
            logger.error("The chosen backend ({}) is currently not "
                         "supported by qgrtsys.".format(backend_name))

            raise ValueError('Undefined backend ({})'.format(backend_name))

        try:
            self.backend = backend_hub.get_instance(backend_name)
        except Exception as e:
            quingo_err("Cannot connect backend '{}' with the following error:".format(backend_name))
            quingo_err("{}".format(e))
            quingo_info("To fix this problem, you could explicitly connect another "
                        "backend use the the following method: \n"
                        "        `if_quingo.connect_backend(<backend_name>)`\n"
                        "    or, install the corresponding simulation backend using:\n"
                        "        `pip install pyqcas`\n"
                        "    or\n"
                        "        `pip install pyqcisim`\n")
            return False

        if self.backend is None:
            msg = "Failed to connect the backend: " + backend_name
            quingo_err(msg)
            logger.error(msg)
        else:
            msg = "successfully connected the backend: " + backend_name
            logger.info(msg)

        self.backend.set_log_level(self.log_level)
        self.backend.set_verbose(self.verbose)
        return True

    def call_quingo(self, qg_filename: str, qg_func_name: str, *args):
        """This function triggers the main process."""
        self.set_call_kernel_success(False)
        success = self.main_process(qg_filename, qg_func_name, *args)
        self.set_call_kernel_success(success)

        return success

    def config_path(self, qg_filename: str, qg_func_name: str):
        '''Configure the following paths of the following files or directories:
            - The project root direcotry (`prj_root_dir`).
            - The build directory (`build_dir`), which is used to buffer generarted files.
                Create this directory if it does not exist.
            - the main file (`main_file_fn`) generated by the runtime system, which contains
                the `main` operation.
            - the qasm file (`qasm_file_path`) generated by the compiler.
        '''
        self.resolved_qg_filename = Path(qg_filename).resolve()

        # ensure there is a build directory in the same directory as the source file.
        self.prj_root_dir = Path(self.resolved_qg_filename).parent
        self.build_dir = self.prj_root_dir / gc.build_dirname

        if self.build_dir.exists():  # clear the existing build directory to remove old files.
            shutil.rmtree(str(self.build_dir))
        self.build_dir.mkdir()       # create a new emtpy build dir.

        # the basename of qg_filename without extension
        self.qg_stem = self.resolved_qg_filename.stem

        self.main_file_fn = (self.build_dir / ('main_' + self.qg_stem)).with_suffix(
            gc.quingo_suffix)

        qasm_fn_no_ext = self.build_dir / qg_func_name
        backend = self.get_backend_or_connect_default()
        qisa_used = backend.get_qisa()
        if qisa_used == 'eqasm':
            self.qasm_file_path = qasm_fn_no_ext.with_suffix(gc.eqasm_suffix)
        elif qisa_used == 'qcis':
            self.qasm_file_path = qasm_fn_no_ext.with_suffix(gc.qcis_suffix)
        else:
            quingo_err("Found unsupported QISA to use: {}".format(qisa_used))
            return False
        return True

    def get_last_qasm(self):
        if self.qasm_file_path is None or not self.qasm_file_path.is_file():
            return ''
        with self.qasm_file_path.open('r') as f:
            return f.read()

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

        if not self.config_path(qg_filename, qg_func_name):
            return False

        if self.verbose:
            quingo_msg("Start compilation ... ", end='')

        # generate the quingo file which contains the main function.
        self.gen_main_func_file(qg_filename, qg_func_name, *args)

        # compile and execute
        if not self.compile():  # compilation failed
            quingo_err("Compilation failed. Abort.")
            return False

        logger.debug("The compiler exited successfully.")

        if not self.qasm_file_path.is_file():
            quingo_err("Error: expected qasm file ({}) has not been generated. Aborts.".format(
                self.qasm_file_path))
            return False

        # compilation finished successfully
        logger.debug("The qasm file has been generated at: {}".format(
            self.qasm_file_path))

        if not self.execute():  # execute the eQASM file
            quingo_err("Execution failed. Abort.")
            return False

        if self.verbose:
            quingo_msg('Execution finished.')

        # read back the results
        self.result = self.get_backend().read_result()

        return True

    def execute(self):
        """This function upload the compiled quantum program, i.e., instruction-format program
        to the backend, and executes it.
        After the execution, the result can be fetched via `read_result()`.
        """
        backend = self.get_backend_or_connect_default()
        if backend.available is False:
            raise EnvironmentError(
                "The backend {} is not available.".format(backend.name()))

        if self.mode == 'state_vector' and not backend.is_simulator():
            raise ValueError("Cannot retrieve state vector from a non-simulator backend.")

        if self.verbose:
            quingo_msg("Uploading the program to the backend {}...".format(backend.name()))

        if not backend.upload_program(self.qasm_file_path):
            quingo_err("Failed to upload the program to the backend {}.".format(backend.name()))
            quingo_info("  Suggestion: are you uploading QCIS program to an eQASM backend "
                        "or eQASM program to a QCIS backend?\n"
                        "    If so, please specify the compiler and backend accordingly.")
            return False

        if self.verbose:
            quingo_msg("Start execution with {}... ".format(backend.name()))

        if backend.name() == "PyQCISim_QuantumSim":
            return backend.execute(self.mode, self.num_shots)
        else:
            return backend.execute()

    def get_imported_qu_fns(self, prj_dir):
        """This function recursively scans the project root directory, and
        return all Quingo files (with extention `.qu` or `.qfg`) as a list."""
        valid_file_list = []
        for r, d, f in os.walk(prj_dir):
            for file in f:
                file_path = Path(r) / file
                if file_path.suffix in ['.qu', '.qfg']:
                    valid_file_list.append(file_path)

        logger.debug("imported files:\n\t" +
                     "\n\t".join(['"{}"'.format(str(f)) for f in valid_file_list]))

        return valid_file_list

    def get_xtext_path(self):
        # TODO: add support of searching quingo.jar
        pass

    def get_compiler_cmd(self, compiler_name):
        assert(compiler_name in self.supported_compilers)

        if compiler_name == 'mlir':
            quingoc_path = distutils.spawn.find_executable('quingoc')
            if quingoc_path is None:
                quingo_err("Cannot find the mlir-based quingoc compiler in the system path.")
                quingo_info("To resolve this problem, you can download quingoc from "
                            "https://gitee.com/hpcl_quanta/quingo-compiler and save "
                            "it at a directory in the system path.")
                return None
            else:
                return quingoc_path

        if compiler_name == 'xtext':
            xtext_path = self.get_xtext_path()
            if xtext_path is None:
                quingo_err("Cannot find the Xtext-based Quingo compiler.")
                quingo_info(
                    "To resolve this issue, please download the quingo.jar from xxxx and configure "
                    "its path using the following command inside python:\n"
                    "     `quingo_interface.set_xtext_compiler_path(<path-to-xtext>)`")
                return None
            return 'java -jar "{}"'.format(xtext_path)

    def compile(self):
        """Compiles the quingo files and generate corresponding quantum assembly code.
            Both the compiler and backend are selected based on the configuration.
        """
        if self.compiler_name is None:
            quingo_info("No Quingo compiler has been set. "
                        "Trying to use the default xtext-based Quingo compiler...")
            self.set_compiler("xtext")

        compiler_name = self.get_compiler()
        compile_cmd_head = self.get_compiler_cmd(compiler_name)
        if compile_cmd_head is None:  # Failure
            return False

        if compiler_name == 'mlir':
            logger.debug(self.compose_mlir_cmd(compile_cmd_head, print=True))
            compile_cmd = self.compose_mlir_cmd(compile_cmd_head, False)

        elif compiler_name == 'xtext':
            # the Quingo files written by the programmer
            # qgrtsys recursively scans the root directory of the project to get all quingo files.
            # however, qgrtsys will only use the files which are imported by `qg_filename`
            user_files = self.get_imported_qu_fns(self.prj_root_dir)

            # default files that every compilation process should process, including:
            #   - a `stand_operations.qu` file, which contains the declaration of opaque operations
            #   - a `config-quingo.qu/.qfg` file, which contains the implementation of the above
            #     operations.
            #
            # If the project directory contains either one of these two files, qgrtsys will the
            # existing file(s). Otherwise, qgrtsys will use the default files as delivered with qgrtsys.
            default_files = []

            fn_list = [f.name for f in user_files]

            # add the file `standard_operations.qu`
            if not gc.std_op_fn in fn_list:
                default_files.append(gc.std_op_full_path)

            # search the file `config-quingo.qfg` in the project directory
            # if not found, use the default one.
            if not gc.std_qfg_fn in fn_list:
                default_files.append(gc.std_qfg_full_path)

            compile_files = [self.main_file_fn]

            user_files.remove(self.main_file_fn)
            compile_files.extend(user_files)
            compile_files.extend(default_files)

            logger.debug(self.compose_xtext_cmd(compile_cmd_head, compile_files, print=True))
            compile_cmd = self.compose_xtext_cmd(compile_cmd_head, compile_files, False)

        else:
            raise ValueError("Found undefined compiler to use.")

        ret_value = subprocess.run(compile_cmd,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   text=True, shell=True)
        if ret_value.stdout != '':
            logger.info(ret_value.stdout.strip())
        if ret_value.stderr != '':
            msg = "Error message from the compiler:\n\t{}".format(
                ret_value.stderr)
            quingo_err(msg)
            logger.error(msg)

        if (ret_value.returncode != 0):  # failure
            return False
        else:  # success
            return True

    def compose_xtext_cmd(self, quingo_compiler, compile_files, print: bool = False):
        if print:
            head = "\n"
            separator = "\n\t "
            str_files = "<imported files>"
        else:
            head = ""
            separator = ""
            str_files = " ".join(['"{}"'.format(str(f))
                                  for f in compile_files])

        compile_cmd = head + quingo_compiler + ' ' + str_files + \
            separator + ' -o "{}"'.format(str(self.qasm_file_path)) + \
            separator + " -s " + str(self.shared_addr) + \
            separator + " -t " + str(self.static_addr) + \
            separator + " -d " + str(self.dynamic_addr) + \
            separator + " -u " + str(self.max_unroll)

        return compile_cmd

    def compose_mlir_cmd(self, quingo_compiler, print: bool = False):
        if print:
            head = "\n"
            separator = "\n\t "
        else:
            head = ""
            separator = ""

        compile_cmd = head + quingo_compiler + ' ' + str(self.main_file_fn) + \
            separator + ' -o "{}"'.format(self.qasm_file_path)

        return compile_cmd

    def gen_main_func_file(self, qg_filename: str, qg_func_name: str, *args):
        """This function generates the main function required to perform
        compilation. A new file named 'main_<qg_filename>' under the
        `<build_dirname>` directory is generated to allocate this main
        function.

        Args:
            qg_filename (str) :  the name of the Quingo file which contains the
                quantum function called by the host program.
            qg_func_name (str) : the name of the Quingo function.
            args (list): a variable length of parameters passed to the quantum function
        """
        qg_file_content = self.resolved_qg_filename.open('r').read()
        main_func_str = self.main_func(qg_filename, qg_func_name, *args)

        try:
            self.main_file_fn.write_text(
                qg_file_content + '\n' + main_func_str)
        except:
            raise IOError("Cannot write the file: ", self.main_file_fn)

    def main_func(self, qg_filename: str, qg_func_name: str, *args):
        """This function is used to generate string version of the main
        function used to call quingo.

        Args:
            qg_func_name (str) : the name of called Quingo operation._name`.
        """

        var_name_list = []
        arg_str_list = []

        logger.debug("calling function '{}' with parameters: {}".format(
            qg_func_name, args))

        if len(args) != 0:
            for (i, arg) in enumerate(args):
                var_name, var_def_str = dt.conv_arg_to_qg_str(i, arg)
                var_name_list.append(var_name)
                arg_str_list.append(var_def_str)

        self.ret_type = get_ret_type(qg_filename, qg_func_name)

        str_params = ", ".join(var_name_list)
        arg_strs = "\n    ".join(arg_str_list)
        if len(arg_strs) > 0:
            arg_strs = "\n    " + arg_strs

        if self.ret_type == 'unit':
            str_ret = ""
        else:
            str_ret = "return "

        func_call = "    {ret}{func_name}({parameters});".format(
            ret=str_ret, func_name=qg_func_name, parameters=str_params)

        func_str = "\noperation main() : {} {{{}\n{}\n}}".format(
            self.ret_type, arg_strs, func_call)

        return func_str

    def config_execution(self, mode: str, num_shots: int = 1):
        '''Configure the execution mode to 'one_shot' or 'state_vector'.
        When the execution mode is 'one_shot', the number of times to run the uploaded quantum
        circuit can be configured using the parameter `num_shots` at the same time.
        '''

        if mode not in ['one_shot', 'state_vector']:
            raise ValueError("Found unrecognized execution mode: '{}'.".format(
                mode) + "Allowed values are: 'one_shot' or 'state_vector'.")

        self.mode = mode
        self.num_shots = num_shots

    def set_num_shots(self, num_shots: int):
        """[Deprecated method]. Set the number of times to run the uploaded quantum circuit in
        simulation. In other words, `num_shots` groups of measurement result will be generated.

        Args:
            num_shots (int): The number of times to run the quantum circuit.
        """
        self.num_shots = num_shots

    def read_result(self, start_addr):
        if self.success_on_last_execution is False:
            quingo_warning('Last execution fails and no result is read back.')
            return None

        qisa_used = self.get_backend().get_qisa()
        if qisa_used == 'eqasm':
            data_trans = dt.Data_transfer()
            data_trans.set_data_block(self.result)
            pydata = data_trans.bin_to_pydata(self.ret_type, start_addr)
            logger.debug(
                "The data converted from the binary is: \n{}\n".format(pydata))
            return pydata

        elif qisa_used == 'qcis':
            return self.result

        else:
            raise ValueError(
                "Reading result from a program with unsupported QISA: {}".format(qisa_used))
