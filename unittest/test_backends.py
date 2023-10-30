from quingo.backend.tequila import QuaLeSim_tequila
from quingo.backend.quantumsim import QuaLeSim_quantumsim
from quingo.backend.symqc import IfSymQC
from quingo.backend.backend_hub import BackendType, Backend_hub
from quingo.backend.qisa import Qisa
from quingo.core.exe_config import *
from pathlib import Path
import threading
import random

cur_dir = Path(__file__).parent
qcis_fn = cur_dir / "test_qcis" / "bell.qcis"
qcis_fn2 = cur_dir / "test_qcis" / "bell_copy.qcis"
quiet_fn = cur_dir / "test_qcis" / "bell.qi"
quiet_fn2 = cur_dir / "test_qcis" / "bell_copy.qi"


def dist(a, b):
    if isinstance(a, complex) and isinstance(b, complex):
        return (a.real - b.real) ** 2 + (a.imag - b.imag) ** 2
    else:
        return (a.evalf() - b.evalf()) ** 2


# progress: 2023-10-09
# finished test on quantumsim and Tequila.
class Test_backends:
    def test_basic(self):
        def single(BackendClass, type, qisa, is_sim):
            sim = BackendClass()
            assert sim.get_type() == type
            assert sim.get_qisa() == qisa
            assert sim.is_simulator() == is_sim

        # QuaLeSim_tequila and QuaLeSim_quantumsim default Qisa type is QCIS
        single(QuaLeSim_tequila, BackendType.TEQUILA, Qisa.QCIS, True)
        single(QuaLeSim_quantumsim, BackendType.QUANTUMSIM, Qisa.QCIS, True)
        single(IfSymQC, BackendType.SYMQC, Qisa.QCIS, True)

    def test_upload_program(self):
        def single(BackendClass, qasm_fn):
            sim = BackendClass()
            try:
                sim.upload_program(qasm_fn)
            except Exception as e:
                assert False, "upload_program failed: {}".format(e)

        single(QuaLeSim_tequila, qcis_fn)
        single(QuaLeSim_tequila, quiet_fn)
        single(QuaLeSim_quantumsim, qcis_fn)
        single(QuaLeSim_quantumsim, quiet_fn)
        single(IfSymQC, qcis_fn)

    def test_execute(self):
        def single(BackendClass, qasm_fn):
            sim = BackendClass()
            sim.upload_program(qasm_fn)
            exe_config = ExeConfig(ExeMode.SimStateVector, 10)
            res = sim.execute(exe_config)
            print(res)
            #assert len(res) == 2
            #assert res[0] == ["Q1", "Q2"]
            #assert all(v in [[0, 0], [1, 1]] for v in res[1])

        single(QuaLeSim_tequila, qcis_fn)
        single(QuaLeSim_quantumsim, qcis_fn)
        #single(QuaLeSim_tequila, quiet_fn)
        #single(QuaLeSim_quantumsim, quiet_fn)
        single(IfSymQC, qcis_fn)

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

        single(QuaLeSim_tequila, qcis_fn)
        single(QuaLeSim_quantumsim, qcis_fn)
        single(QuaLeSim_tequila, quiet_fn)
        single(QuaLeSim_quantumsim, quiet_fn)
        single(IfSymQC, qcis_fn)

    def test_get_from_hub(self):
        def single(backend_type, qasm_fn):
            hub = Backend_hub()
            sim = hub.get_instance(backend_type)
            sim.upload_program(qasm_fn)
            exe_config = ExeConfig(ExeMode.SimFinalResult, 10)
            res = sim.execute(exe_config)
            assert res[0] == ["Q1", "Q2"]
            assert len(res[1]) == 10
            assert all(v in [[0, 0], [1, 1]] for v in res[1])

        single(BackendType.TEQUILA, qcis_fn)
        single(BackendType.QUANTUMSIM, qcis_fn)
        single(BackendType.TEQUILA, quiet_fn)
        single(BackendType.QUANTUMSIM, quiet_fn)
        single(BackendType.SYMQC, qcis_fn)

    def test_state_vector(self):
        def single(backend_type, qasm_fn):
            hub = Backend_hub()
            sim = hub.get_instance(backend_type)
            sim.upload_program(qasm_fn)
            exe_config = ExeConfig(ExeMode.SimStateVector, 1)
            res = sim.execute(exe_config)
            a = res["quantum"][1][0]
            b = res["quantum"][1][3]

            assert res["quantum"][0] == ["Q1", "Q2"]
            assert dist(a, b) <= 0.01

        single(BackendType.TEQUILA, quiet_fn2)
        single(BackendType.QUANTUMSIM, quiet_fn2)
        single(BackendType.TEQUILA, qcis_fn)
        single(BackendType.QUANTUMSIM, qcis_fn)
        single(BackendType.SYMQC, qcis_fn)

    def single_sim(backend_type, qcis_fn, exp_res):
        hub = Backend_hub()
        sim = hub.get_instance(backend_type)
        sim.upload_program(qcis_fn)
        exe_config = ExeConfig(ExeMode.SimFinalResult)
        sim_result = sim.execute(exe_config)
        _, msmt_res = sim_result
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

        single(BackendType.TEQUILA)
        single(BackendType.QUANTUMSIM)


if __name__ == "__main__":
    test = Test_backends()
    # test.test_basic()
    # test.test_upload_program()
    test.test_execute()
    #test.test_shots()
    #test.test_get_from_hub()
    #test.test_state_vector()
    # test.test_sim_in_paral()
