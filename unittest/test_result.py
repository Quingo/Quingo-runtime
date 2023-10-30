from quingo.backend.tequila import QuaLeSim_tequila
from quingo.backend.quantumsim import QuaLeSim_quantumsim
from quingo.backend.symqc import IfSymQC
from quingo.backend.backend_hub import BackendType, Backend_hub
from quingo.backend.qisa import Qisa
from quingo.core.exe_config import *
from pathlib import Path
import sympy
import threading
import random

cur_dir = Path(__file__).parent
qcis_fn = cur_dir / "test_qcis" / "bell.qcis"
qcis_fn2 = cur_dir / "test_qcis" / "bell_copy.qcis"
quiet_fn = cur_dir / "test_qcis" / "bell.qi"
quiet_fn2 = cur_dir / "test_qcis" / "bell_copy.qi"


def is_similar_statevector(m1, m2):
    if isinstance(m1, sympy.matrices.dense.MutableDenseMatrix):
        m1 = [complex(i.evalf()) for i in m1]
    if isinstance(m2, sympy.matrices.dense.MutableDenseMatrix):
        m2 = [complex(i.evalf()) for i in m2]
    dist = 0
    for i in range(len(m1)):
        dist = dist + (m1[i].real - m2[i].real) ** 2 + (m1[i].imag - m2[i].imag) ** 2
    return dist <= 1e-5


class Test_backends:
    def test_one_shot_res(self):
        def single(BackendClass, qasm_fn, num_shots):
            sim = BackendClass()
            sim.upload_program(qasm_fn)
            exe_config = ExeConfig(ExeMode.SimFinalResult, num_shots)
            res = sim.execute(exe_config)
            assert isinstance(res, tuple)
            assert len(res) == 2
            assert res[0] == ["Q1", "Q2"]
            assert len(res[1]) == num_shots
            assert all(v in [[0, 0], [1, 1]] for v in res[1])
            return res

        res1 = single(QuaLeSim_tequila, qcis_fn, 10)
        res2 = single(QuaLeSim_quantumsim, qcis_fn, 8)
        res3 = single(IfSymQC, qcis_fn, 1)
        assert res1[0] == res2[0]
        assert res2[0] == res3[0]

    def test_state_vector_res(self):
        def single(BackendClass, qasm_fn):
            sim = BackendClass()
            sim.upload_program(qasm_fn)
            num_shots = 10
            exe_config = ExeConfig(ExeMode.SimStateVector)
            res = sim.execute(exe_config)
            print(res)
            assert res["quantum"][0] == ["Q1", "Q2"]
            return res

        res1 = single(QuaLeSim_tequila, qcis_fn)
        res2 = single(QuaLeSim_quantumsim, qcis_fn)
        res3 = single(IfSymQC, qcis_fn)
        assert is_similar_statevector(res1["quantum"][1], res2["quantum"][1])
        assert is_similar_statevector(res2["quantum"][1], res3["quantum"][1])


if __name__ == "__main__":
    test = Test_backends()
    test.test_one_shot_res()
    # test.test_state_vector_res()
