from pathlib import Path
from utils import quingo_err
import quingo.global_config as gc


def set_compiler_path(path_str, is_mlir=False):
    path = Path(path_str)
    if path_str.startswith('~'):
        path = path.expanduser()
    if not path.exists():
        quingo_err("cannot find the compiler at {}".format(path_str))
        return False

    if is_mlir:
        fn = 'mlir_compiler_path.txt'
        path_file = Path(__file__).parent / fn
    else:
        path_file = gc.xtext_compiler_config_path

    with path_file.open('w') as f:
        f.write(path_str)

    return True


def set_xtext_compiler_path(xtext_path_str):
    set_compiler_path(xtext_path_str, False)
