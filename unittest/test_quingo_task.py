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

class TestQuingoTask2:
    def test_init(self):
        mock_fn = qu_dir / "mock.qu"
        task = Quingo_task(mock_fn, "foo")
        assert task.called_qu_fn == mock_fn
        assert task.called_func == "foo"
        assert task.debug_mode == False
        assert task.qubits_info == None
        assert task._backend == BackendType.QUANTUM_SIM
        assert task._qisa == None
        assert task.build_dir is not None

    def test_qubits_info(self):
        mock_fn = qu_dir / "mock.qu"
        task = Quingo_task(mock_fn, "foo", qubits_info="qubits_info")
        assert task.qubits_info == "qubits_info"

    def test_cl_entry_fn(self):
        mock_fn = qu_dir / "mock.qu"
        task = Quingo_task(mock_fn, "foo")
        assert task.cl_entry_fn.stem == "main_mock_foo"

    def test_build_dir(self):
        mock_fn = qu_dir / "mock.qu"
        task = Quingo_task(mock_fn, "foo", debug_mode=True)
        assert task.build_dir.samefile(Path.cwd() / gc.build_dirname)
        task = Quingo_task(mock_fn, "foo", debug_mode=False)
        assert str(task.build_dir).startswith("/tmp")

    def test_qisa_type(self):
        mock_fn = qu_dir / "mock.qu"
        task = Quingo_task(mock_fn, "foo", backend=BackendType.QUANTUM_SIM)
        assert task.qisa_type == Qisa.QCIS
        task = Quingo_task(mock_fn, "foo", backend=BackendType.QUANTIFY)
        assert task.qisa_type == Qisa.Quantify

    def test_called_qu_dir(self):
        mock_fn = qu_dir / "mock.qu"
        task = Quingo_task(mock_fn, "foo")
        assert task.called_qu_dir == mock_fn.parent

    def test_include_dir(self):
        mock_fn = qu_dir / "mock.qu"
        task = Quingo_task(mock_fn, "foo")
        assert task.called_qu_dir in task.include_dir
        assert task.build_dir in task.include_dir


if __name__ == "__main__":
    TestQuingoTask().test_init_1()
    TestQuingoTask().test_init_2()
    TestQuingoTask().test_infer_qisa()
