import pytest
from quingo.backend.backend_hub import BackendType
from quingo.backend.qualesim import QuaLeSim
from quingo.core.exe_config import ExeConfig, ExeMode
from quingo import execute
from quingo.utils import number_distance
from pathlib import Path


unittest_dir = Path(__file__).parent / ".."
bell_qcis_fn = unittest_dir / "test_qcis" / "bell.qcis"
bell_no_msmt_qcis_fn = unittest_dir / "test_qcis" / "bell_no_msmt.qcis"

bell_quiet_fn = unittest_dir / "test_qcis" / "bell.qi"
bell_no_msmt_quiet_fn = unittest_dir / "test_qcis" / "bell_no_msmt.qi"


bell_qasm_fns = [
    bell_qcis_fn,
    bell_quiet_fn,
]


@pytest.fixture(
    scope="module",
    params=[BackendType.QUALESIM_QUANTUMSIM, BackendType.QUALESIM_TEQUILA],
)
def get_backend_type(request):
    return request.param


@pytest.fixture(scope="module")
def get_qualesim(get_backend_type):
    backend_type = get_backend_type
    return QuaLeSim(backend_type)


@pytest.fixture(params=bell_qasm_fns)
def get_bell_qasm_fn(request):
    return request.param


def test_call_qualesim(get_qualesim, get_bell_qasm_fn):
    simulator = get_qualesim
    simulator.upload_program(get_bell_qasm_fn)
    num_shots = 10
    exe_config = ExeConfig(ExeMode.SimShots, num_shots)
    names, result = simulator.execute(exe_config)
    assert names == ["Q1", "Q2"]
    assert len(result) == num_shots
    assert all(i == j for i, j in result)
