from quingo import *
from pathlib import Path


qu_file = Path(__file__).parent / "kernel.qu"


def SimQuantumsim(circ_name):
    task = Quingo_task(qu_file, circ_name)
    cfg = ExeConfig(ExeMode.SimStateVector)
    qasm_fn = compile(task, params=(), config_file="")
    res = execute(qasm_fn, BackendType.QUANTUM_SIM, cfg)
    print("sim res for bell state is:")
    print("classical:", res["classical"])
    print("quantum:", res["quantum"])


SimQuantumsim("bell_state")
