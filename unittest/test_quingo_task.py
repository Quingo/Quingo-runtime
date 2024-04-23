import pytest
from quingo.core.quingo_task import *
from quingo.backend.backend_hub import BackendType
from quingo.backend.qisa import Qisa
from pathlib import Path
import platform


unittest_dir = Path(__file__).parent
qu_dir = unittest_dir / "test_qu"


class TestQuingoTask:
    def test_init_1(self):
        mock_fn = qu_dir / "mock.qu"
        task = Quingo_task(mock_fn, "foo")
        assert task.called_qu_fn.samefile(mock_fn)
        assert task.called_func == "foo"
        assert task.debug_mode == False
        assert task.called_qu_dir.samefile(qu_dir)
        assert qu_dir in task.include_dir
        os_name = platform.system()
        if os_name in ["Linux", "Darwin"]:
            assert str(task.build_dir).startswith("/tmp")
        assert task.build_dir in task.include_dir
        assert task.called_qu_dir in task.include_dir
        assert task.cl_entry_fn.stem == "main_mock_foo"
        assert task.qisa_type == Qisa.QCIS

    def test_init_2(self):
        mock_fn = qu_dir / "mock.qu"
        task = Quingo_task(mock_fn, "bar", debug_mode=True)
        assert task.called_qu_fn.samefile(mock_fn)
        assert task.called_func == "bar"
        assert task.debug_mode == True
        assert task.called_qu_dir.samefile(qu_dir)
        assert qu_dir in task.include_dir
        # os_name = platform.system()
        # print(task.build_dir)
        # print(cur_dir / gc.build_dirname)
        # assert task.build_dir.samefile(cur_dir / gc.build_dirname)
        assert task.build_dir in task.include_dir
        assert task.called_qu_dir in task.include_dir
        assert task.cl_entry_fn.stem == "main_mock_bar"

    def test_infer_qisa(self):
        def single_test(backend, qisa):
            mock_fn = qu_dir / "mock.qu"
            task = Quingo_task(mock_fn, "foo", backend=backend)
            assert task.qisa_type == qisa

        single_test(BackendType.SYMQC, Qisa.QCIS)
        single_test(BackendType.TEQUILA, Qisa.QCIS)
        single_test(BackendType.QUANTUM_SIM, Qisa.QCIS)
        # single_test(BackendType.QUALESIM_TEQUILA, Qisa.QCIS)
        # single_test(BackendType.QUALESIM_QUANTUMSIM, Qisa.QCIS)
        single_test(BackendType.XIAOHONG, Qisa.QCIS)
        single_test(BackendType.QUANTIFY, Qisa.Quantify)


if __name__ == "__main__":
    TestQuingoTask().test_init_1()
    TestQuingoTask().test_init_2()
    TestQuingoTask().test_infer_qisa()
