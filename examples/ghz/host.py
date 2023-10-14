import logging
from quingo import *
from pathlib import Path

qu_file = Path(__file__).parent / "kernel.qu"


def routine(circ_name, num_shots=1, num_qubits=1):
    task = Quingo_task(qu_file, circ_name)
    cfg = ExeConfig(ExeMode.SimFinalResult, num_shots)
    res = call(task, (num_qubits,), BackendType.DQCSIM_QUANTUMSIM, cfg)
    print("sim res:", res)


routine("ghz", 4, 5)
routine("ghz", 4, 4)
routine("ghz", 4, 3)
