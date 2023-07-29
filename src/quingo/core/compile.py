import subprocess
from quingo.core.quingo_task import Quingo_task
from pathlib import Path
from .compiler_config import get_mlir_path
from quingo.core.utils import quingo_err, get_logger
from quingo.if_backend.qisa import *
from quingo.core.preparation import gen_main_file


logger = get_logger((__name__).split(".")[-1])


def compile(task: Quingo_task, params: tuple, qasm_fn: Path = None):
    """Compile the quingo file with given parameters and return the path of
    the generated qasm file.
    """
    gen_main_file(task.called_qu_fn, task.called_func, task.cl_entry_fn, params)

    if qasm_fn is None:
        suffix = get_suffix(task.qisa_type)
        qasm_fn = task.cl_entry_fn.with_suffix(suffix)

    quingoc_path = Path(get_mlir_path())

    compile_cmd = compose_cl_cmd(task, qasm_fn, quingoc_path)
    logger.debug(compile_cmd)
    ret_value = subprocess.run(
        compile_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=True,
    )
    if ret_value.stdout != "":
        logger.info(ret_value.stdout.strip())
    if ret_value.stderr != "":
        msg = "Error message from the compiler:\n\t{}".format(ret_value.stderr)
        quingo_err(msg)
        logger.error(msg)

    if ret_value.returncode != 0:  # failure
        raise RuntimeError(
            "failed to compile the Quingo source file: {}".format(task.called_qu_fn)
        )
    else:
        return qasm_fn


def compose_cl_cmd(task: Quingo_task, qasm_fn: Path, quingoc_path: Path):
    cl_path = '"{}"'.format(str(quingoc_path.resolve()))
    cl_entry_fn = '"{}"'.format(str(task.cl_entry_fn))

    opt_inc_dirs = " ".join(['-I "{}"'.format(str(dir)) for dir in task.include_dir])
    opt_isa = "--isa={}".format(get_qisa_name(task.qisa_type))

    qubits_info = ""
    if task.qisa_type == Qisa.Quantify:
        qubits_info = '--qubits="{}"'.format(str(task.qubits_info.resolve()))
    opt_qubit_map = qubits_info

    if isinstance(qasm_fn, str):
        qasm_fn = Path(qasm_fn).resolve()
    opt_out_fn = '-o "{}"'.format(str(qasm_fn.resolve()))

    cmd_eles = [cl_path, cl_entry_fn, opt_inc_dirs, opt_isa, opt_qubit_map, opt_out_fn]

    compile_cmd = " ".join([ele for ele in cmd_eles if ele.strip() != ""])

    return compile_cmd
