from quingo.backend.backend_hub import BackendType, Backend_hub
from quingo.core.exe_config import ExeConfig, ExeMode
from quingo import execute
from quingo.utils import number_distance
from pathlib import Path
import pytest

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


class TestStateVector:
    """When simulating a quantum program in the state vector mode,
    the result should be a tuple:
        (
            ["Q1", "Q2"],
            [0.7071067811865475, 0.0, 0.0, 0.7071067811865475]
        )
    """

    def vec_tests(self):
        def vec_test_without_msmt(simulator):
            exe_config = ExeConfig(ExeMode.SimStateVector)
            state_vec_res = execute(bell_no_msmt_qcis_fn, simulator, exe_config)
            assert len(state_vec_res) == 2
            assert state_vec_res[0] == ["Q1", "Q2"]

            assert len(state_vec_res[1]) == 4

        vec_test_without_msmt(BackendType.TEQUILA)
        vec_test_without_msmt(BackendType.QUANTUM_SIM)
        vec_test_without_msmt(BackendType.SYMQC)
        vec_test_without_msmt(BackendType.QUALESIM_QUANTUMSIM)

    def vec_tests_with_msmt(self):

        def vec_test_with_msmt(simulator):
            exe_config = ExeConfig(ExeMode.SimStateVector)
            state_vec_res = execute(bell_qcis_fn, simulator, exe_config)
            assert len(state_vec_res) == 2
            assert state_vec_res[0] == ["Q1", "Q2"]

            assert len(state_vec_res[1]) == 4

        vec_test_with_msmt(BackendType.TEQUILA)
        vec_test_with_msmt(BackendType.QUANTUM_SIM)
        vec_test_with_msmt(BackendType.SYMQC)
        vec_test_with_msmt(BackendType.QUALESIM_QUANTUMSIM)

    def test_quantumsim_with_msmt(self):
        exe_config = ExeConfig(ExeMode.SimStateVector)
        state_vec_res = execute(
            bell_no_msmt_qcis_fn, BackendType.QUANTUM_SIM, exe_config
        )
        assert len(state_vec_res) == 2
        assert state_vec_res[0] == ["Q1", "Q2"]

        assert len(state_vec_res[1]) == 4


if __name__ == "__main__":
    # test_final_result_with_msmt()
    test_shot_without_msmt(BackendType.QUANTUM_SIM, 10)
    # test = TestFinalResult()
    # # test.test_sim_with_msmt()
    # # test.test_sim_without_msmt()

    # # test = TestStateVector()
    # # test.test_symqc_with_msmt()
    # # test.test_symqc_without_msmt()
    # # test.test_quantumsim_with_msmt()
    # test = TestShots()
    # test.test_shots()
