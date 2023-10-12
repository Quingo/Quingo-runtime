from quingo import *
from pathlib import Path


qu_file = Path(__file__).parent / "kernel.qu"


def routine(circ_name, num_shots=1):
    task = Quingo_task(qu_file, circ_name)
    cfg = ExeConfig(ExeMode.SimStateVector, 3)
    # exemod 1
    res = call(task, (), BackendType.DQCSIM_QUANTUMSIM, cfg)
    # exemod2
    qasm_fn = compile(task, params=())
    res = execute(qasm_fn, BackendType.DQCSIM_QUANTUMSIM, cfg)
    print("sim res for bell state is:")
    print("classical:", res["classical"])
    print("quantum:", res["quantum"])
    # res = execute(qasm_fn, BackendType.DQCSIM_TEQUILA, cfg)
    # print("sim res: ", res)
    # res = execute(qasm_fn, BackendType.SYMQC, cfg)
    # print("sim res: ", res)


routine("bell_state", 10)
