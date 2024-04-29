from quingo import *
from pathlib import Path


qu_file = Path(__file__).parent / "kernel.qu"


def SimStateVector(circ_name):
    task = Quingo_task(qu_file, circ_name)
    cfg = ExeConfig(ExeMode.SimStateVector)
    qasm_fn = compile(task, params=(), config_file="")
    res = execute(qasm_fn, BackendType.QUANTUM_SIM, cfg)
    print(res)


SimStateVector("bell_state")
