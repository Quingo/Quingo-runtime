from quingo import *
from pathlib import Path


qu_file = Path(__file__).parent / "kernel.qu"


def routine(circ_name, num_shots=1):
    task = Quingo_task(qu_file, circ_name)
    cfg = ExeConfig(
        ExeMode.RealMachine,
        num_shots,
        xh_login_key="946dbe920c1b048a8ae7e3475d2184f4",
        xh_machine_name="Xiaohong",
    )
    qasm_fn = compile(task, params=(), config_file="", target="qcloud_sh")
    res = execute(qasm_fn, BackendType.XIAOHONG, cfg)
    print("result: ", res)


routine("bell_state", 10)
