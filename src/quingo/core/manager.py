from __future__ import annotations
from numpy.typing import NDArray
from typing import List, Union
import numpy as np
import array
import sympy as sp

from pathlib import Path

from quingo.core.exe_config import ExeConfig, ExeMode
from quingo.core.quingo_task import Quingo_task
from quingo.core.compile import compile
from quingo.backend.backend_hub import BackendType, Backend_hub


def verify_backend_config(backend: BackendType, exe_config: ExeConfig) -> bool:
    """Check if the combination of backend and execution configuration is valid."""
    if (backend == BackendType.XIAOHONG) and (exe_config.mode != ExeMode.RealMachine):
        return False

    if backend == BackendType.QUANTIFY:
        return False
    return True


def execute(
    qasm_fn: Path, be_type: BackendType, exe_config: ExeConfig = ExeConfig()
) -> Union[List | NDArray]:
    """Execute the quingo task on the specified backend and return the result."""

    if not verify_backend_config(be_type, exe_config):
        raise ValueError(
            "Error configuration {} on the backend {}".format(str(exe_config), backend)
        )

    backend = Backend_hub().get_instance(be_type)
    backend.upload_program(qasm_fn)
    result = backend.execute(exe_config)
    if exe_config.mode == ExeMode.SimStateVector:
        names, array_values = result
        if len(names) == 0:
            return ([], 1)

        if isinstance(array_values, list):
            if len(array_values) == 0:
                return ([], 1)

            array_values = np.array(array_values)

        elif isinstance(array_values, array.array):
            array_values = np.array(array_values)

        elif isinstance(array_values, sp.Matrix):
            array_values = np.array(array_values).astype(np.complex64)

        else:
            assert isinstance(array_values, np.ndarray)

        array_values = array_values.flatten()
        return (names, array_values)

    return result


def call(
    task: Quingo_task,
    params: tuple,
    be_type: BackendType = BackendType.QUANTUM_SIM,
    exe_config: ExeConfig = ExeConfig(),
    config_fn="",
):
    """Execute the quingo task on the specified backend and return the result."""

    qasm_fn = compile(task, params, config_file=config_fn)
    return execute(qasm_fn, be_type, exe_config)
