from quingo.backend.pyqcisim_quantumsim import PyQCISim_quantumsim
from pathlib import Path
from quingo.backend.qisa import Qisa
from quingo.backend.backend_hub import BackendType
from quingo.core.exe_config import *

cur_dir = Path(__file__).parent
qcis_fn = cur_dir / "test_qcis" / "bell.qcis"


class Test_quantumsim:
    def test_basic(self):
        qsim = PyQCISim_quantumsim()
        assert qsim.get_type() == BackendType.QUANTUM_SIM
        assert qsim.get_qisa() == Qisa.QCIS
        assert qsim.is_simulator() == True

    def test_upload_program(self):
        qsim = PyQCISim_quantumsim()
        try:
            qsim.upload_program(qcis_fn)
        except Exception as e:
            assert False, "upload_program failed: {}".format(e)

    def test_execute(self):
        qsim = PyQCISim_quantumsim()
        qsim.upload_program(qcis_fn)
        exe_config = ExeConfig()
        res = qsim.execute(exe_config)
        print(res)


if __name__ == "__main__":
    test = Test_quantumsim()
    test.test_basic()
    test.test_upload_program()
    test.test_execute()
