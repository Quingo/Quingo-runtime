from quingo import *
from pathlib import Path


qu_file = Path(__file__).parent / "kernel.qu"


def routine(circ_name, num_shots=1):
    task = Quingo_task(qu_file, circ_name)
    cfg = ExeConfig(
        ExeMode.RealMachine,
        num_shots,
        xh_login_key="mptXLbxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        xh_machine_name="gd_test",
        exp_name="exp_bell",
    )
    qasm_fn = compile(task, params=(), config_file="", target="qcloud_sh")
    res = execute(qasm_fn, BackendType.CTEK, cfg)
    print("result: ", res)


routine("bell_state", 10)
