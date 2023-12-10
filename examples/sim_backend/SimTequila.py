from quingo import *
from pathlib import Path


qu_file = Path(__file__).parent / "kernel.qu"


def SimTequila(circ_name, num_shots=1):
    task = Quingo_task(qu_file, circ_name)
    cfg = ExeConfig(ExeMode.SimFinalResult, num_shots)
    qasm_fn = compile(task, params=(), config_file="")
    res = execute(qasm_fn, BackendType.TEQUILA, cfg)  # QuantumSim, SymQC
    print("sim res: ", res)


SimTequila("bell_state", 10)
