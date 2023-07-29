from quingo.backend.pyqcisim_tequila import PyQCISim_tequila
from pathlib import Path
from quingo.backend.qisa import Qisa
from quingo.backend.backend_hub import BackendType
from quingo.core.exe_config import *

cur_dir = Path(__file__).parent
qcis_fn = cur_dir / "test_qcis" / "bell.qcis"


class Test_tequila:
    def test_basic(self):
        tequila = PyQCISim_tequila()
        assert tequila.get_type() == BackendType.TEUQILA
        assert tequila.get_qisa() == Qisa.QCIS
        assert tequila.is_simulator() == True

    def test_upload_program(self):
        tequila = PyQCISim_tequila()
        try:
            tequila.upload_program(qcis_fn)
        except Exception as e:
            assert False, "upload_program failed: {}".format(e)

    def test_execute(self):
        tequila = PyQCISim_tequila()
        tequila.upload_program(qcis_fn)
        exe_config = ExeConfig()
        res = tequila.execute(exe_config)
        print(res)


if __name__ == "__main__":
    test = Test_tequila()
    test.test_basic()
    test.test_upload_program()
    test.test_execute()
