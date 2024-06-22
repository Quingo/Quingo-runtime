import pytest
from pathlib import Path
from quingo.backend.pyqcisim_tequila import PyQCISim_tequila
from quingo.core.exe_config import ExeConfig, ExeMode


# @pytest.fixture(
#     scope="module",
#     params=[BackendType.TEQUILA],
# )
# def get_backend_type(request):
#     return request.param


@pytest.fixture(scope="module")
def get_tequila():
    return PyQCISim_tequila()


unittest_dir = Path(__file__).parent / ".."


@pytest.fixture(scope="module", params=[unittest_dir / "test_qcis" / "bell.qcis"])
def get_bell_qasm_fn(request):
    return request.param


def test_call_tequila(get_tequila, get_bell_qasm_fn):
    simulator = get_tequila
    simulator.upload_program(get_bell_qasm_fn)
    exe_config = ExeConfig(ExeMode.SimProbability)
    names, p0s = simulator.execute(exe_config)
    assert names == ["Q1", "Q2"]
    assert len(p0s) == len(names)
    assert all(p0 == pytest.approx(0.5) for p0 in p0s)
