from pathlib import Path
from quingo import BackendType, Quingo_task, ExeConfig, ExeMode
from quingo import call, compile, execute

unittest_dir = Path(__file__).parent
qu_file = unittest_dir / "test_qu" / "bell.qu"


def test_compile_execute():
    task = Quingo_task(qu_file, "bell")
    num_shot = 4
    cfg = ExeConfig(ExeMode.SimShots, num_shot)
    qasm_fn = compile(task, params=())
    res = execute(qasm_fn, BackendType.QUANTUM_SIM, cfg)

    assert len(res[0]) == 2
    assert len(res[1]) == 4


def test_call():
    task = Quingo_task(qu_file, "bell")
    cfg = ExeConfig(ExeMode.SimShots, 4)
    res = call(task, (), BackendType.QUANTUM_SIM, cfg)

    assert len(res[0]) == 2
    assert len(res[1]) == 4


if __name__ == "__main__":
    test_compile_execute()
    test_call()
