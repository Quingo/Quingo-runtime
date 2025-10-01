import logging
import subprocess
from pathlib import Path

from quingo.backend.qisa import Qisa, get_qisa_name, get_suffix
from quingo.core.compiler_config import get_mlir_path
from quingo.core.preparation import gen_main_file
from quingo.core.quingo_logger import get_logger, quingo_err
from quingo.core.quingo_task import Quingo_task
from quingo.utils import ensure_path

logger = get_logger((__name__).split(".")[-1])


def compile(task: Quingo_task, params: tuple, qasm_fn: Path = None, **kwargs):
    """Compile the quingo file with given parameters and return the path of
    the generated qasm file.
    """
    if "config_file" in kwargs:
        config_file = kwargs["config_file"]
    else:
        config_file = ""
    if "target" in kwargs:
        target = kwargs["target"]
    else:
        target = ""
    if "chip_path" in kwargs:
        chip_path = kwargs["chip_path"]
    else:
        chip_path = ""

    logger.setLevel(logging.INFO)
    gen_main_file(task.called_qu_fn, task.called_func, task.cl_entry_fn, params)

    if qasm_fn is None:
        suffix = get_suffix(task.qisa_type)
        qasm_fn = task.cl_entry_fn.with_suffix(suffix)
        mq_fn = task.cl_entry_fn.with_suffix(".json")
    else:
        qasm_fn = ensure_path(qasm_fn)
        mq_fn = qasm_fn.stem + ".json"
        mq_fn = ensure_path(mq_fn)

    quingoc_path = Path(get_mlir_path())

    compile_cmd = compose_cl_cmd(
        task, qasm_fn, quingoc_path, config_file, target, chip_path, mq_fn
    )
    if task.debug_mode:
        logger.info(compile_cmd)
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


def compose_cl_cmd(
    task: Quingo_task,
    qasm_fn: Path,
    quingoc_path: Path,
    configfile="",
    target="",
    chip_path="",
    mq_fn="",
):
    qasm_fn = ensure_path(qasm_fn)
    quingoc_path = ensure_path(quingoc_path)

    cl_path = '"{}"'.format(str(quingoc_path.resolve()))
    cl_entry_fn = '"{}"'.format(str(task.cl_entry_fn))

    opt_inc_dirs = " ".join(['-I "{}"'.format(str(dir)) for dir in task.include_dir])
    opt_isa = "--isa={}".format(get_qisa_name(task.qisa_type))

    qubits_info = ""
    if task.qisa_type == Qisa.Quantify:
        qubits_info = '--qubits="{}"'.format(str(task.qubits_info.resolve()))
    opt_qubit_map = qubits_info

    opt_out_fn = '-o "{}"'.format(str(qasm_fn))

    config_fn = '--config-fn="{}"'.format(str(configfile)) if len(configfile) > 0 else ""

    chip_path_ = '--chip-config="{}"'.format(str(chip_path)) if len(chip_path) > 0 else ""

    target_ = '--target="{}"'.format(str(target)) if len(target) > 0 else ""
    # mq_path = '--mq-path="{}"'.format(str(mq_fn))

    cmd_eles = [
        cl_path,
        "-u",
        cl_entry_fn,
        opt_inc_dirs,
        config_fn,
        chip_path_,
        target_,
        # mq_path,
        opt_isa,
        opt_qubit_map,
        opt_out_fn,
    ]

    compile_cmd = " ".join([ele for ele in cmd_eles if ele.strip() != ""])

    return compile_cmd
