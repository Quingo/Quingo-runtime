from quingo import *
from pathlib import Path


qu_file = Path(__file__).parent / "kernel.qu"


def SimFinalResult(circ_name, num_shots=1):
    task = Quingo_task(qu_file, circ_name)
    cfg = ExeConfig(ExeMode.SimFinalResult, num_shots)
    qasm_fn = compile(task, params=(), config_file="")
    res = execute(qasm_fn, BackendType.DQCSIM_TEQUILA, cfg)  # QuantumSim, SymQC
    print("sim res: ", res)


def SimStateVector(circ_name):
    task = Quingo_task(qu_file, circ_name)
    cfg = ExeConfig(ExeMode.SimStateVector)
    qasm_fn = compile(task, params=(), config_file="")
    res = execute(qasm_fn, BackendType.DQCSIM_QUANTUMSIM, cfg)
    print("sim res for bell state is:")
    print("classical:", res["classical"])
    print("quantum:", res["quantum"])


def routine(circ_name, num_shots=1):
    task = Quingo_task(qu_file, circ_name)
    cfg = ExeConfig(ExeMode.SimFinalResult, num_shots)
    res = call(task, (), BackendType.SYMQC, cfg)
    print("sim res: ", res)


SimFinalResult("bell_state", 10)
# SimStateVector("bell_state")
# routine("bell_state", 5)
