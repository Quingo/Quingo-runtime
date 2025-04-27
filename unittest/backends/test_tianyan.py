from pathlib import Path

from quingo.backend.backend_hub import BackendType
from quingo.backend.qisa import Qisa
from quingo.backend.tianyan import ZDXLZ_Tianyan
from quingo.core.exe_config import *

cur_dir = Path(__file__).parent
qcis_fn = cur_dir / ".." / "test_qcis" / "bell_cz.qcis"


def test_execute():
    platform = ZDXLZ_Tianyan()
    platform.upload_program(qcis_fn)
    exe_config = ExeConfig(
        mode=ExeMode.RealMachine,
        num_shots=1000,
        qcloud_platform_login_key="55kGV2wrhSuZjzhR+rmhhiavICd+KYZo9WmHav8+4ng=",
        qcloud_machine_name="tianyan24",
    )
    res = platform.execute(exe_config)
    print(res)


if __name__ == "__main__":
    test_execute()
