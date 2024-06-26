from quingo import *
from pathlib import Path


qu_file = Path(__file__).parent / "bell.qu"


def test_xiaohong(circ_name, num_shots):
    task = Quingo_task(qu_file, circ_name)
    cfg = ExeConfig(
        ExeMode.RealMachine,
        num_shots,
        xh_login_key="946dbe920c1b048a8ae7e3475d2184f4",
        xh_machine_name="Xiaohong",
    )
    qasm_fn = compile(task, params=(), config_file="", target="qcloud_sh")
    
    backend = Backend_hub()
    print("Backend: ", backend.backends[BackendType.XIAOHONG][1])
    print("Execution Mode: ", cfg)
    print("Totol Num of Execution: ", cfg.num_shots)
    
    # res = execute(qasm_fn, BackendType.XIAOHONG, cfg)
    # print(res)
    


test_xiaohong("bell_state", 20)
