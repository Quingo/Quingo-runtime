import pytest
from quingo.core.quingo_task import *
from pathlib import Path
from quingo.core.compile import *
from quingo.core.compiler_config import get_mlir_path

unittest_dir = Path(__file__).parent
qu_dir = unittest_dir / "test_qu"
mock_qcis_fn = unittest_dir / "mock.qcis"


class TestGetMlirPath:
    def test_get_path(self):
        mlir_path = get_mlir_path()
        assert mlir_path is not None


class TestCompileCmd:
    def test_gen_default(self):
        mock_fn = qu_dir / "mock.qu"
        task = Quingo_task(mock_fn, "foo")

        qasm_fn = compile(task, params=(1, 2), qasm_fn=mock_qcis_fn)

        mlir_path = Path(get_mlir_path())
        cmd = compose_cl_cmd(task, qasm_fn, mlir_path)
        cmd_eles = cmd.split()
        assert len(cmd_eles) == 10
        assert mlir_path.resolve().samefile(cmd_eles[0].strip('"'))
        assert cmd_eles[1] == '"{}"'.format(task.cl_entry_fn.resolve())
        assert cmd_eles[2] == "-I"
        assert cmd_eles[4] == "-I"
        assert cmd_eles[7] == "--isa=qcis"
        assert cmd_eles[8] == "-o"
        # assert Path(qasm_fn).samefile(cmd_eles[8].strip('"'))

    def test_compile(self):
        bell_fn = qu_dir / "bell.qu"
        task = Quingo_task(bell_fn, "bell", debug_mode=True)
        qasm_fn = compile(task, ())
        with qasm_fn.open("r") as f:
            lines = f.readlines()
        assert lines[0].strip().split() == ["H", "Q0"]
        assert lines[1].strip().split() == ["CNOT", "Q0", "Q1"]

    def test_compile2(self):
        bell_fn = qu_dir / "bell.qu"
        task = Quingo_task(bell_fn, "bell")
        qasm_fn = compile(task, (), qasm_fn=unittest_dir / "out_bell.qcis")
        assert qasm_fn.samefile(unittest_dir / "out_bell.qcis")
        with qasm_fn.open("r") as f:
            lines = f.readlines()
        assert lines[0].strip().split() == ["H", "Q0"]
        assert lines[1].strip().split() == ["CNOT", "Q0", "Q1"]


if __name__ == "__main__":
    # TestGetMlirPath().test_get_path()
    # TestCompileCmd().test_gen_default()
    TestCompileCmd().test_compile()
    # TestCompileCmd().test_compile2()
