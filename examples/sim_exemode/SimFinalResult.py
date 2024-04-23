from quingo import *
from pathlib import Path


qu_file = Path(__file__).parent / "kernel.qu"


def SimFinalResult(circ_name):
    task = Quingo_task(qu_file, circ_name)
    cfg = ExeConfig(ExeMode.SimFinalResult)
    qasm_fn = compile(task, params=(), config_file="")
    res = execute(qasm_fn, BackendType.QUANTUM_SIM, cfg)  # QuantumSim, SymQC
    print("sim res: ", res)


SimFinalResult("bell_state")
