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
        num_shots=10,
        qcloud_platform_login_key="95hoNFTHmKqtXNi5gGUAjS7As2l8xm5Ymze1DHZFJx4=",
        qcloud_machine_name="tianyan_sw",
    )
    results = platform.execute(exe_config)
    # assert isinstance(results, list)
    # res = results[0]
    # assert "resultStatus" in list(res.keys())
    # assert "probability" in list(res.keys())
    # assert (
    #     len(res["probability"]) == 2
    #     and "00" in res["probability"]
    #     and "11" in res["probability"]
    # )


if __name__ == "__main__":
    test_execute()
