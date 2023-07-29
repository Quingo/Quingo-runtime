from quingo.backend.symqc import IfSymQC
from pathlib import Path
from quingo.backend.qisa import Qisa
from quingo.backend.backend_hub import BackendType
from quingo.core.exe_config import *

cur_dir = Path(__file__).parent
qcis_fn = cur_dir / "test_qcis" / "bell.qcis"


class Test_symqc:
    def test_basic(self):
        tequila = IfSymQC()
        assert tequila.get_type() == BackendType.SYMQC
        assert tequila.get_qisa() == Qisa.QCIS
        assert tequila.is_simulator() == True

    def test_upload_program(self):
        tequila = IfSymQC()
        try:
            tequila.upload_program(qcis_fn)
        except Exception as e:
            assert False, "upload_program failed: {}".format(e)

    def test_execute(self):
        tequila = IfSymQC()
        tequila.upload_program(qcis_fn)
        exe_config = ExeConfig()
        res = tequila.execute(exe_config)
        print(res)


if __name__ == "__main__":
    test = Test_symqc()
    test.test_basic()
    test.test_upload_program()
    test.test_execute()
