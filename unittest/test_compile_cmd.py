import pytest
from quingo.core.quingo_task import *
from pathlib import Path
from quingo.core.compile import *
from quingo.core.compiler_config import get_mlir_path
from global_config import SRC_PATH

cur_dir = SRC_PATH / "unittest" / ""
qu_dir = cur_dir / "test_qu" / ""


class TestGetMlirPath:
    def test_get_path(self):
        mlir_path = get_mlir_path()
        assert mlir_path is not None


class TestCompileCmd:
    def test_gen_default(self):
        mock_fn = qu_dir / "mock.qu"
        task = Quingo_task(mock_fn, "foo")
        mlir_path = Path(get_mlir_path())
        qasm_fn = compile(
            task,
            (
                1,
                2,
            ),
            qasm_fn=cur_dir / "mock.qcis",
        )
        cmd = compose_cl_cmd(
            task,
            qasm_fn,
            mlir_path,
        )
        cmd_eles = cmd.split()
        print(cmd_eles)
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
        task = Quingo_task(bell_fn, "bell")
        qasm_fn = compile(task, ())
        with qasm_fn.open("r") as f:
            lines = f.readlines()
        assert lines[0].strip() == "H    Q0"
        assert lines[2].strip() == "CZ    Q0           Q1"

    def test_compile2(self):
        bell_fn = qu_dir / "bell.qu"
        task = Quingo_task(bell_fn, "bell")
        qasm_fn = compile(task, (), qasm_fn=cur_dir / "out_bell.qcis")
        assert qasm_fn.samefile(cur_dir / "out_bell.qcis")
        with qasm_fn.open("r") as f:
            lines = f.readlines()
        assert lines[0].strip() == "H    Q0"
        assert lines[2].strip() == "CZ    Q0           Q1"


if __name__ == "__main__":
    # TestGetMlirPath().test_get_path()
    TestCompileCmd().test_gen_default()
    # TestCompileCmd().test_compile()
    # TestCompileCmd().test_compile2()
