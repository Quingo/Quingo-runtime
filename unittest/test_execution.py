from pathlib import Path
from quingo.core.manager import call, compile, execute
from quingo.core.exe_config import *
from quingo.core.quingo_task import Quingo_task
from quingo.backend.backend_hub import BackendType, Backend_hub

qu_file = Path(__file__).parent / "test_qu" / "bell.qu"


class Test_execution:
    def test_execute(self):
        task = Quingo_task(qu_file, "bell_state")
        num_shot = 4
        cfg = ExeConfig(ExeMode.SimFinalResult, num_shot)
        qasm_fn = compile(task, params=())
        res = execute(qasm_fn, BackendType.QUANTUM_SIM, cfg)

        assert len(res[0]) == 2
        assert len(res[1]) == 4

    def test_call(self):
        task = Quingo_task(qu_file, "bell_state")
        cfg = ExeConfig(ExeMode.SimFinalResult, 4)
        res = call(task, (), BackendType.QUANTUM_SIM, cfg)

        assert len(res[0]) == 2
        assert len(res[1]) == 4


if __name__ == "__main__":
    test = Test_execution()
    test.test_execute()
    test.test_call()
