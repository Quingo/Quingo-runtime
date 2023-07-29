from quingo import *
from pathlib import Path


qu_file = Path(__file__).parent / "test_qu" / "bell.qu"


class test_execution:
    def test_execute(self):
        task = Quingo_task(qu_file, "bell_state")
        num_shot = 10
        cfg = ExeConfig(ExeMode.SimFinalResult, num_shot)
        qasm_fn = compile(task, params=())
        res = execute(qasm_fn, BackendType.QUANTUM_SIM, cfg)

        assert len(res[0]) == 2
        assert len(res[1]) == 4
        s = sum([v for k, v in res[1].items()])
        assert s == num_shot

    def test_call(self):
        task = Quingo_task(qu_file, "bell_state")
        cfg = ExeConfig(ExeMode.SimFinalResult, 10)
        res = call(task, (), BackendType.QUANTUM_SIM, cfg)

        assert len(res[0]) == 2
        assert len(res[1]) == 4
        s = sum([v for k, v in res[1].items()])


if __name__ == "__main__":
    test = test_execution()
    test.test_execute()
    test.test_call()
