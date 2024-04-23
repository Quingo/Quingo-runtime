import logging
from quingo import *
from pathlib import Path

qu_file = Path(__file__).parent / "kernel.qu"

# configure the circ_name
circ_name = "ghz"

# configure the execution mode
num_shots = 4
cfg = ExeConfig(ExeMode.SimShots, num_shots)

# the input param num_qubits
num_qubits = 5


task = Quingo_task(qu_file, circ_name)
res = call(task, (num_qubits,), BackendType.QUANTUM_SIM, cfg)
print("sim res:", res)
