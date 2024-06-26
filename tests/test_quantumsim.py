from quingo import *
from pathlib import Path


qu_file = Path(__file__).parent / "bell.qu"


def test_quantumsim(circ_name, num_shots=10):
    task = Quingo_task(qu_file, circ_name, )
    cfg = ExeConfig(ExeMode.SimShots, num_shots=num_shots)
    qasm_fn = compile(task, params=(), config_file="")
    sim_result = execute(qasm_fn, BackendType.QUANTUM_SIM, cfg)
    measure_states = sim_result[1]
    backend = Backend_hub().backends[BackendType.QUANTUM_SIM]
    print("Backend: ", backend[1])
    print("measure_states: ", measure_states)
    

test_quantumsim("bell_state", 10)
