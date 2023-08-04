from pathlib import Path
from quingo import *
from quingo.backend.qisa import Qisa

qu_file = Path(__file__).parent / "test_qu" / "quiets_test.qu"

task = Quingo_task(qu_file, "test", qisa=Qisa.QUIET)
num_shot = 10
cfg = ExeConfig(ExeMode.SimFinalResult, num_shot)

qasm_fn = Path(__file__).parent / "test.qi"

compile(task, params=(), qasm_fn=qasm_fn)
res = execute(qasm_fn, BackendType.DQCSIM_TEQUILA, cfg)

print(res)