from pathlib import Path
from quingo import *


# get ansatz.
def get_ansatz(qu_file, circ_name, backend, params, config_file=""):
    task = Quingo_task(qu_file, circ_name, debug_mode=False)
    qasm_fn = compile(task, params=params, config_file=config_file)
    res = execute(qasm_fn, backend, ExeConfig(ExeMode.SimStateVector))
    return [i for i in res["quantum"][1]]
