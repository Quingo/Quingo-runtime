from quingo.backend.backend_hub import BackendType, Backend_hub
from quingo.core.exe_config import ExeConfig, ExeMode
from quingo import execute
from quingo.utils import number_distance, state_fidelity
from pathlib import Path
import pytest
import numpy as np

cur_dir = Path(__file__).parent

bell_qcis_fn = cur_dir / ".." / "test_qcis" / "bell.qcis"
bell_no_msmt_qcis_fn = cur_dir / ".." / "test_qcis" / "bell_no_msmt.qcis"


quiet_fn = cur_dir / ".." / "test_qcis" / "bell.qi"
quiet_fn2 = cur_dir / ".." / "test_qcis" / "bell_no_msmt.qi"


backends = [
    BackendType.QUANTUM_SIM,
    BackendType.TEQUILA,
    BackendType.QUALESIM_QUANTUMSIM,
    BackendType.SYMQC,
]
num_shots = [5, 10]


@pytest.fixture(params=backends)
def get_simulator(request):
    return request.param


@pytest.fixture(params=num_shots)
def get_num_shots(request):
    return request.param


def test_shot_with_msmt(get_simulator, get_num_shots):
    simulator = get_simulator
    num_shots = get_num_shots

    exe_config = ExeConfig(ExeMode.SimShots, num_shots)
    names, result = execute(bell_qcis_fn, simulator, exe_config)
    print("result for {}: ".format(simulator), names, result)
    assert names == ["Q1", "Q2"]
    assert len(result) == num_shots
    assert all(i == j for i, j in result)


def test_shot_without_msmt(get_simulator, get_num_shots):
    simulator = get_simulator
    num_shots = get_num_shots

    exe_config = ExeConfig(ExeMode.SimShots, num_shots)
    names, result = execute(bell_no_msmt_qcis_fn, simulator, exe_config)
    assert names == []
    assert len(result) == num_shots
    assert all(len(l) == 0 for l in result)


def test_final_result_with_msmt(get_simulator, get_num_shots):
    simulator = get_simulator
    num_shots = get_num_shots

    exe_config = ExeConfig(ExeMode.SimFinalResult, num_shots=num_shots)
    result = execute(bell_qcis_fn, simulator, exe_config)
    print("result: ", result)


def test_final_result_without_msmt(get_simulator, get_num_shots):
    simulator = get_simulator
    num_shots = get_num_shots

    exe_config = ExeConfig(ExeMode.SimFinalResult, num_shots=num_shots)
    result = execute(bell_no_msmt_qcis_fn, simulator, exe_config)
    print("result: ", result)


def test_state_vector_without_msmt(get_simulator):
    simulator = get_simulator
    exe_config = ExeConfig(ExeMode.SimStateVector)
    qubit_names, state_vec = execute(bell_no_msmt_qcis_fn, simulator, exe_config)

    assert qubit_names == ["Q1", "Q2"]
    assert isinstance(state_vec, (list, np.ndarray))
    assert state_vec.shape == (4,)
    assert state_fidelity(
        state_vec, [0.7071067811865475, 0.0, 0.0, 0.7071067811865475]
    ) == pytest.approx(1)


def test_state_vector_with_msmt(get_simulator):
    simulator = get_simulator
    exe_config = ExeConfig(ExeMode.SimStateVector)
    qubit_names, state_vec = execute(bell_qcis_fn, simulator, exe_config)

    assert qubit_names == ["Q1", "Q2"]
    assert isinstance(state_vec, (list, np.ndarray))
    assert state_vec.shape == (4,)
    assert state_fidelity(
        state_vec, [0.7071067811865475, 0.0, 0.0, 0.7071067811865475]
    ) == pytest.approx(1)
