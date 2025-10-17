from __future__ import annotations
from numpy.typing import NDArray
from typing import List, Union, Tuple
import numpy as np
import array
import sympy as sp
import logging
import tempfile

from pathlib import Path

from quingo.core.exe_config import ExeConfig, ExeMode
from quingo.core.quingo_task import Quingo_task
from quingo.core.compile import compile
from quingo.backend.backend_hub import BackendType, Backend_hub
from quingo.core.quingo_logger import get_logger
from quingo.utils import validate_path
from quingo.lib.qiskit_tools import estimate_resource

logger = get_logger((__name__).split(".")[-1])


def verify_backend_config(backend: BackendType, exe_config: ExeConfig) -> bool:
    """Check if the combination of backend and execution configuration is valid."""
    if (backend == BackendType.XIAOHONG) and (exe_config.mode != ExeMode.RealMachine):
        return False

    if backend == BackendType.QUANTIFY:
        return False
    return True


def execute(
    qasm_fn_or_str: Path,
    be_type: BackendType,
    exe_config: ExeConfig = ExeConfig(),
    debug_mode=False,
) -> Union[List, NDArray, Tuple[Union[List, NDArray], Tuple]]:
    """Execute the quingo task on the specified backend and return the result.

    If exe_config.enable_resource_estimation is True, returns a tuple of
    (result, resource_estimation) where resource_estimation is a tuple of
    (depth, num_qubits, ops_count).
    """
    logger.setLevel(logging.INFO)

    if not verify_backend_config(be_type, exe_config):
        raise ValueError(
            "Error configuration {} on the backend {}".format(str(exe_config), backend)
        )

    if debug_mode:
        execute_info = "execute the following program with backend {}: \n {}".format(
            str(be_type.name), str(qasm_fn_or_str)
        )
        logger.info(execute_info)

    backend = Backend_hub().get_instance(be_type)

    qasm_fn = validate_path(qasm_fn_or_str)
    if qasm_fn is None:
        backend.upload_program_str(qasm_fn_or_str)
    else:
        backend.upload_program(qasm_fn)

    result = backend.execute(exe_config)
    if exe_config.mode == ExeMode.SimStateVector:
        names, array_values = result
        if len(names) == 0:
            result = ([], 1)
        else:
            if isinstance(array_values, list):
                if len(array_values) == 0:
                    result = ([], 1)
                else:
                    array_values = np.array(array_values)

            elif isinstance(array_values, array.array):
                array_values = np.array(array_values)

            elif isinstance(array_values, sp.Matrix):
                array_values = np.array(array_values).astype(np.complex64)

            else:
                assert isinstance(array_values, np.ndarray)

            array_values = array_values.flatten()
            result = (names, array_values)

    # Perform resource estimation if requested
    if exe_config.enable_resource_estimation:
        # Determine if qasm_fn_or_str is a file path or a string
        if qasm_fn is not None:
            # It's a valid file path
            # Check if the file is a QCIS file
            if qasm_fn.suffix.lower() != ".qcis":
                logger.warning(
                    f"资源统计仅支持 QCIS 格式文件，当前文件类型为 {qasm_fn.suffix}，跳过资源统计"
                )
                return result
            resource_info = estimate_resource(qasm_fn)
        else:
            # It's a string, write to temporary file
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".qcis", delete=False
            ) as tmp_file:
                tmp_file.write(qasm_fn_or_str)
                tmp_path = Path(tmp_file.name)

            try:
                resource_info = estimate_resource(tmp_path)
            finally:
                # Clean up temporary file
                tmp_path.unlink()

        return (result, resource_info)

    return result


def call(
    task: Quingo_task,
    params: tuple,
    be_type: BackendType = BackendType.QUANTUM_SIM,
    exe_config: ExeConfig = ExeConfig(),
    **kwargs,
):
    """Execute the quingo task on the specified backend and return the result."""

    qasm_fn = compile(task, params, **kwargs)
    return execute(qasm_fn, be_type, exe_config, debug_mode=task.debug_mode)
