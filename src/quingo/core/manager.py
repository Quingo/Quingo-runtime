from .exe_config import *
from quingo.backend.backend_hub import BackendType, Backend_hub
import quingo.core.data_transfer as dt
from pathlib import Path
from quingo.core.utils import (
    quingo_err,
    quingo_msg,
    quingo_warning,
    get_logger,
    quingo_info,
)
from quingo.backend.qisa import *

logger = get_logger((__name__).split(".")[-1])


def verify_backend_config(backend: BackendType, exe_config: ExeConfig) -> bool:
    """Check if the combination of backend and execution configuration is valid."""
    if backend == BackendType.ZUCHONGZHI and is_simulation(exe_config.mode):
        return False

    if backend == BackendType.QUANTIFY:
        return False
    return True


def execute(qasm_fn: Path, be_type: BackendType, exe_config: ExeConfig = None):
    """Execute the quingo task on the specified backend and return the result."""

    if verify_backend_config(backend, exe_config) is False:
        raise ValueError(
            "Error configuration {} on the backend {}".format(str(exe_config), backend)
        )

    backend = Backend_hub().get_backend(be_type)

    backend.upload_program(qasm_fn)

    return backend.execute(exe_config)


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
            "Reading result from a program with unsupported QISA: {}".format(qisa_used)
        )
