from quingo.backend.pyqcisim_quantumsim import PyQCISim_quantumsim
from quingo.backend.pyqcisim_tequila import PyQCISim_tequila
from quingo.backend.dqcsim_tequila import DQCsim_tequila
from quingo.backend.symqc import IfSymQC
from pathlib import Path
from quingo.backend.qisa import Qisa
from quingo.backend.backend_hub import BackendType, Backend_hub
from quingo.core.exe_config import *
import threading
import random

cur_dir = Path(__file__).parent
qcis_fn = cur_dir / "test_qcis" / "bell.qcis"
quiet_fn = cur_dir / "test_qcis" / "bell.qi"


# progress: 2023-08-02
# finished test on quantumsim and Tequila.
# TODO: modify the result format of SymQC to match the runtime system regulation.
class Test_backends:
    def test_basic(self):
        def single(BackendClass, type, qisa, is_sim):
            sim = BackendClass()
            assert sim.get_type() == type
            assert sim.get_qisa() == qisa
            assert sim.is_simulator() == is_sim

        single(PyQCISim_tequila, BackendType.TEUQILA, Qisa.QCIS, True)
        single(PyQCISim_quantumsim, BackendType.QUANTUM_SIM, Qisa.QCIS, True)
        single(IfSymQC, BackendType.SYMQC, Qisa.QCIS, True)
        single(DQCsim_tequila, BackendType.DQCSIM_TEQUILA, Qisa.QUIET, True)

    def test_upload_program(self):
        def single(BackendClass, qasm_fn):
            sim = BackendClass()
            try:
                sim.upload_program(qasm_fn)
            except Exception as e:
                assert False, "upload_program failed: {}".format(e)

        single(PyQCISim_tequila, qcis_fn)
        single(PyQCISim_quantumsim, qcis_fn)
        single(IfSymQC, qcis_fn)
        single(DQCsim_tequila, quiet_fn)

    def test_execute(self):
        def single(BackendClass, qasm_fn):
            sim = BackendClass()
            sim.upload_program(qasm_fn)
            exe_config = ExeConfig()
            res = sim.execute(exe_config)
            assert len(res) == 2
            assert res[0] == ["Q1", "Q2"]
            assert all(v in [[0, 0], [1, 1]] for v in res[1])

        single(PyQCISim_tequila, qcis_fn)
        single(PyQCISim_quantumsim, qcis_fn)
        single(DQCsim_tequila, quiet_fn)
        # single(IfSymQC)

    def test_shots(self):
        def single(BackendClass, qasm_fn):
            random_vals = [3, 10, 100]
            for num_rep in random_vals:
                sim = BackendClass()
                sim.upload_program(qasm_fn)
                exe_config = ExeConfig(ExeMode.SimFinalResult, num_rep)
                res = sim.execute(exe_config)
                assert res[0] == ["Q1", "Q2"]
                assert len(res[1]) == num_rep
                assert all(v in [[0, 0], [1, 1]] for v in res[1])

        single(PyQCISim_tequila, qcis_fn)
        single(PyQCISim_quantumsim, qcis_fn)
        single(DQCsim_tequila, quiet_fn)
        # single(IfSymQC)

    def test_get_from_hub(self):
        def single(backend_type):
            hub = Backend_hub()
            sim = hub.get_instance(backend_type)
            sim.upload_program(qcis_fn)
            exe_config = ExeConfig(ExeMode.SimFinalResult, 10)
            res = sim.execute(exe_config)
            assert res[0] == ["Q1", "Q2"]
            assert len(res[1]) == 10
            assert all(v in [[0, 0], [1, 1]] for v in res[1])

        single(BackendType.TEUQILA)
        single(BackendType.QUANTUM_SIM)
        single(DQCsim_tequila)
        # single(BackendType.SYMQC)

    def single_sim(backend_type, qcis_fn, exp_res):
        hub = Backend_hub()
        tequila = hub.get_instance(backend_type)
        tequila.upload_program(qcis_fn)
        exe_config = ExeConfig(ExeMode.SimFinalResult)
        sim_result = tequila.execute(exe_config)
        _, msmt_res = sim_result
        # print("sim_result: ", sim_result)
        res = msmt_res[0]
        res.reverse()
        int_res = int("".join(map(str, res)), 2)
        assert int_res == exp_res

    def test_sim_in_paral(self):
        def single(backend_type):
            qcis_2_fn = cur_dir / "test_qcis" / "mod_adder_nc_res_2.qcis"
            qcis_5_fn = cur_dir / "test_qcis" / "mod_adder_nc_res_5.qcis"

            t1 = threading.Thread(
                target=Test_backends.single_sim,
                args=(backend_type, qcis_2_fn, 2),
            )
            t2 = threading.Thread(
                target=Test_backends.single_sim,
                args=(backend_type, qcis_5_fn, 5),
            )
            t1.start()
            t2.start()

        single(BackendType.TEUQILA)
        single(BackendType.QUANTUM_SIM)
        # single(BackendType.SYMQC)


if __name__ == "__main__":
    test = Test_backends()
    test.test_basic()
    test.test_upload_program()
    test.test_execute()
    test.test_shots()
    test.test_get_from_hub()
    test.test_sim_in_paral()
