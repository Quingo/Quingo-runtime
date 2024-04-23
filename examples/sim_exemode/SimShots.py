from quingo import *
from pathlib import Path


qu_file = Path(__file__).parent / "kernel.qu"


def SimShots(circ_name, num_shots=1):
    task = Quingo_task(qu_file, circ_name)
    cfg = ExeConfig(ExeMode.SimShots, num_shots)
    qasm_fn = compile(task, params=(), config_file="")
    res = execute(qasm_fn, BackendType.QUANTUM_SIM, cfg)  # QuantumSim, SymQC
    print("sim res: ", res)


SimShots("bell_state", 10)
