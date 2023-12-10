from quingo import *
from pathlib import Path


qu_file = Path(__file__).parent / "kernel.qu"


def routine(circ_name, num_shots=1):
    task = Quingo_task(qu_file, circ_name)
    cfg = ExeConfig(ExeMode.SimFinalResult, 10)
    # exemod 1
    res = call(task, (), BackendType.QUANTUM_SIM, cfg)
    print("sim res: ", res)
    # exemod2
    # qasm_fn = compile(task, params=())
    # res = execute(qasm_fn, BackendType.QUANTUM_SIM, cfg)
    # print("sim res: ", res)
    # res = execute(qasm_fn, BackendType.TEQUILA, cfg)
    # print("sim res: ", res)
    # res = execute(qasm_fn, BackendType.SYMQC, cfg)
    # print("sim res: ", res)


routine("main_ctrl", 10)
