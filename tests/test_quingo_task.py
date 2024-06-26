from quingo import *
from pathlib import Path


qu_file = Path(__file__).parent / "bell.qu"


def test_quingo(circ_name, num_shots=1):
    task = Quingo_task(qu_file, circ_name)
    cfg = ExeConfig(ExeMode.SimFinalResult, num_shots=num_shots)
    qasm_fn = compile(task, params=(), config_file="")
    sim_result = execute(qasm_fn, BackendType.QUALESIM_QUANTUMSIM, cfg)
    
    print("Backend: ", Backend_hub().backends[BackendType.QUALESIM_QUANTUMSIM][1])
    print(sim_result)


test_quingo("bell_state", 10)
