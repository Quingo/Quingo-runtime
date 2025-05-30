from quingo import *
from pathlib import Path


qu_file = Path(__file__).parent / "kernel.qu"


def routine(circ_name, num_shots=1):
    task = Quingo_task(qu_file, circ_name, debug_mode=True)
    cfg = ExeConfig(ExeMode.SimFinalResult, num_shots=num_shots)
    qasm_fn = compile(task, params=(), config_file="", target="qcloud_sh")
    sim_result = execute("./bell_state.qcis", BackendType.TEQUILA, cfg)
    print(sim_result)
    names, values = sim_result
    # print("sim res: ", res)
    print("names: ", names)
    print("values ({}): ".format(type(values)), values)


routine("bell_state", 10)
