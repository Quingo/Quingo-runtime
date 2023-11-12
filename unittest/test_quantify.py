from pathlib import Path
from quingo.backend.qisa import Qisa
from quingo.backend.backend_hub import BackendType
from quingo.core.exe_config import *
from quingo.core.quingo_task import *

cur_dir = Path(__file__).parent
kernel_file = cur_dir / "test_qu" / "t1.qu"


class Test_compile_quantify:
    def test_basic(self):
        task = Quingo_task(kernel_file, "t1", backend=BackendType.QUANTIFY)
        assert task.qisa_type == Qisa.Quantify
