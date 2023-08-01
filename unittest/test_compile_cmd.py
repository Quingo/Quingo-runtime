import pytest
from quingo.core.quingo_task import *
from pathlib import Path
from quingo.core.compile import *

from quingo.core.compiler_config import get_mlir_path

cur_dir = Path(__file__).parent


class TestGetMlirPath:
    def test_get_path(self):
        mlir_path = get_mlir_path()
        assert mlir_path is not None


class TestCompileCmd:
    def test_gen_default(self):
        task = Quingo_task("mock.qu", "foo")
        mlir_path = Path(get_mlir_path())
        cmd = compose_cl_cmd(
            task,
            "mock.qasm",
            mlir_path,
        )
        cmd_eles = cmd.split()
        print(cmd_eles)
        assert len(cmd_eles) == 9
        assert mlir_path.resolve().samefile(cmd_eles[0].strip('"'))
        assert cmd_eles[1] == '"{}"'.format(task.cl_entry_fn.resolve())
        assert cmd_eles[2] == "-I"
        assert cmd_eles[4] == "-I"
        assert cmd_eles[6] == "--isa=qcis"
        assert cmd_eles[7] == "-o"
        assert Path("mock.qasm").samefile(cmd_eles[8].strip('"'))

    def test_compile(self):
        bell_fn = cur_dir / "bell.qu"
        task = Quingo_task(bell_fn, "bell")
        qasm_fn = compile(task, (1,))
        with qasm_fn.open("r") as f:
            lines = f.readlines()
        assert lines[0].strip() == "H    Q1"
        assert lines[1].strip() == "CNOT    Q1           Q2"

    def test_compile2(self):
        bell_fn = cur_dir / "bell.qu"
        task = Quingo_task(bell_fn, "bell")
        qasm_fn = compile(task, (1,), qasm_fn="out_bell.qcis")
        assert qasm_fn.samefile("out_bell.qcis")
        with qasm_fn.open("r") as f:
            lines = f.readlines()
        assert lines[0].strip() == "H    Q1"
        assert lines[1].strip() == "CNOT    Q1           Q2"


if __name__ == "__main__":
    TestGetMlirPath().test_get_path()
    TestCompileCmd().test_gen_default()
    TestCompileCmd().test_compile()
    TestCompileCmd().test_compile2()
