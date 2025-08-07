from pathlib import Path

qgrtsys_root_dir = Path(__file__).absolute().parent  # corresponds to `<quingo-runtime>/src/quingo`
qgrtsys_repo_dir = qgrtsys_root_dir.parent.parent  # corresponds to `<quingo-runtime>`

mlir_compiler_config_path = qgrtsys_root_dir / "core" / "mlir_compiler_path.txt"

default_mlir_compiler_path = Path.home() / ".quingo" / "quingoc"

std_op_fn = "standard_operations.qu"
std_qfg_fn = "config-quingo.qfg"
std_op_full_path = qgrtsys_root_dir / "lib" / std_op_fn
std_qfg_full_path = qgrtsys_root_dir / "lib" / std_qfg_fn


quingo_suffix = ".qu"
eqasm_suffix = ".eqasm"
qcis_suffix = ".qcis"
quantify_suffix = ".json"
res_bin_suffix = ".bin"
build_dirname = "build"

shared_mem_start_addr = 0x000
shared_mem_size = 0x100000

QU_BOOL_SIZE = 1
QU_INT_SIZE = 4
QU_PTR_SIZE = 4
QU_DOUBLE_SIZE = 4

allowed_primitive_types = ["int", "bool", "double", "time"]
allowed_python_types = [
    "int",
    "bool",
    "float",
    "float32",
    "float64",
    "list",
    "tuple",
    "ndarray",
    "Time",
]

endian = "little"
