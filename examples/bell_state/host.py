from quingo import *
from pathlib import Path


qu_file = Path(__file__).parent / "kernel.qu"


def routine(circ_name, num_shots=1):
    task = Quingo_task(qu_file, circ_name)
    cfg = ExeConfig(ExeMode.SimFinalResult, 10)
    # qasm_fn = compile(task, params=())
    # res = execute(qasm_fn, BackendType.QUANTUM_SIM, cfg)
    res = call(task, (), BackendType.SYMQC, cfg)
    print("sim res: ", res)


routine("bell_state", 10)
