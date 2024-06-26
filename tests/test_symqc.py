from quingo import *
from pathlib import Path


qu_file = Path(__file__).parent / "bell.qu"


def test_symqc(circ_name, num_shots=10):
    task = Quingo_task(qu_file, circ_name, )
    cfg = ExeConfig(ExeMode.SimShots, num_shots=num_shots)
    qasm_fn = compile(task, params=(), config_file="")
    sim_result = execute(qasm_fn, BackendType.SYMQC, cfg)
    
    # 提取测量结果
    measure_states = sim_result[1]
    
    # 获取使用的后端
    backend = Backend_hub().backends[BackendType.SYMQC]
    print("Backend: ", backend[1])
    print("QISA TYPE: ", get_qisa_name(backend[3]).upper())
    print("measure_states: ", measure_states)
    

test_symqc("bell_state", 10)
