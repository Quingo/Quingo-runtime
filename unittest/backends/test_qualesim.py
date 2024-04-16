from quingo.backend import QuaLeSim_quantumsim
from quingo.core.exe_config import ExeConfig, ExeMode
from quingo import execute
from quingo.utils import number_distance
from pathlib import Path


unittest_dir = Path(__file__).parent / ".."
bell_qcis_fn = unittest_dir / "test_qcis" / "bell.qcis"
bell_no_msmt_qcis_fn = unittest_dir / "test_qcis" / "bell_no_msmt.qcis"

bell_quiet_fn = unittest_dir / "test_qcis" / "bell.qi"
bell_no_msmt_quiet_fn = unittest_dir / "test_qcis" / "bell_no_msmt.qi"


class TestQuaLeSimQuantumSim:
    def test_qcis(self):
        simulator = QuaLeSim_quantumsim()
        simulator.upload_program(bell_qcis_fn)
        num_shots = 10
        exe_config = ExeConfig(ExeMode.SimShots, num_shots)
        names, result = simulator.execute(exe_config)
        assert names == ["Q1", "Q2"]
        assert len(result) == num_shots
        assert all(i == j for i, j in result)

    def test_quiet(self):
        simulator = QuaLeSim_quantumsim()
        simulator.upload_program(bell_quiet_fn)
        num_shots = 10
        exe_config = ExeConfig(ExeMode.SimShots, num_shots)
        names, result = simulator.execute(exe_config)
        assert names == ["Q1", "Q2"]
        assert len(result) == num_shots
        assert all(i == j for i, j in result)
