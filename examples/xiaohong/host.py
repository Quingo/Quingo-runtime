from quingo import *
from pathlib import Path


qu_file = Path(__file__).parent / "kernel.qu"


def routine(circ_name, num_shots=1):
    task = Quingo_task(qu_file, circ_name)
    cfg = ExeConfig(
        ExeMode.RealMachine,
        num_shots,
        xh_login_key="7e6999bab11453428b8ded1fac00b3ea",
        xh_machine_name="Transponder",
    )
    qasm_fn = compile(task, params=(), config_file="")
    res = execute(qasm_fn, BackendType.XIAOHONG, cfg)
    print("result: ", res)


routine("bell_state", 10)
