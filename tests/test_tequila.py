from quingo import *
from pathlib import Path


qu_file = Path(__file__).parent / "bell.qu"


def test_tequila(circ_name, num_shots=1):
    task = Quingo_task(qu_file, circ_name)
    cfg = ExeConfig(ExeMode.SimShots, num_shots=num_shots)
    qasm_fn = compile(task, params=(), config_file="")
    
    # Construct the tequila backend.
    tequila_backend = Backend_hub().get_instance(BackendType.TEQUILA)
    
    # uplaod the compiled qasm file to the backend.
    tequila_backend.upload_program(qasm_fn)
    
    # execute the task on tequila backend.
    sim_result = tequila_backend.execute(cfg)
    
    print(sim_result)


test_tequila("bell_state", 10)
