from pathlib import Path
import shutil
import quingo.global_config as gc
import tempfile
from quingo.backend.backend_hub import BackendType
from quingo.backend.qisa import Qisa
from quingo.core.utils import ensure_path

DEBUG_MODE = False


def create_empty_dir(dir_path: Path):
    if dir_path.exists():
        shutil.rmtree(str(dir_path))
    dir_path.mkdir()


class Quingo_task:
    def __init__(self, called_qu_fn: Path, called_func: str, **kwargs) -> None:
        """
        Define a quingo task by specifying the quingo file and the entry function.

        Note, this task only stores the following five elements:
        - the path of the called Quingo file (called_qu_fn)
        - the name of the entry function (called_func)
        - the path of the build directory (build_dir)
        - debug_mode
        - the target qisa (qisa) if specified upon initialization
        - the target backend (backend) if specified upon initialization

        If `qisa` and `backend` are not specified, then the value of them will be infered
        when required.

        The `build_dir` is calculated at the first time it is called. If the debug mode is
        on, then the build_dir is under the same directory as the called Quingo file.
        Otherwise, the build_dir is a temporary directory.

        Except them, all other properties are calculated when they are called. By doing so,
        only a minimal amount of information is stored in the task object, which reduces the
        risk of inconsistency when using this object.
        """
        # file name and function name
        called_qu_fn = ensure_path(called_qu_fn)
        self._called_qu_fn = called_qu_fn
        self._called_func = called_func
        self._build_dir = None

        self._qubits_info = kwargs.get("qubits_info", None)
        self.debug_mode = kwargs.get("debug_mode", False)
        # qisa and backend
        self._qisa = kwargs.get("qisa", None)
        self._backend = kwargs.get("backend", BackendType.QUANTUM_SIM)

    @property
    def qubits_info(self):
        """The path of the qubits information file."""
        return self._qubits_info

    @property
    def cl_entry_fn(self):
        """Generate the name of the Quingo file that is used to contain the main function."""
        main_qu_stem = "main_" + self.called_qu_fn.stem + "_" + self.called_func
        _cl_entry_fn = (self.build_dir / main_qu_stem).with_suffix(gc.quingo_suffix)
        return _cl_entry_fn

    @property
    def called_func(self):
        """The name of the called function."""
        return self._called_func

    @property
    def called_qu_fn(self):
        """The path of the called Quingo file."""
        return self._called_qu_fn

    @property
    def build_dir(self):
        """The path of the build directory.

        - In Debug mode, the build directory is under the current directory.
        - Otherwise, the build directory is a temporary directory.
        """
        # since build_dir can be a temporary directory, we need to record it instead of
        # calculating it every time.
        if self._build_dir is not None:
            return self._build_dir

        if self.debug_mode:  # debug mode create `build` dir under the current dir
            self._build_dir = Path.cwd() / gc.build_dirname
            create_empty_dir(self._build_dir)

        else:
            self._build_dir = Path(tempfile.mkdtemp())

        return self._build_dir

    @property
    def qisa_type(self):
        """
        Infer the qisa type from the selected backend.
        """
        if self._qisa is not None:
            return self._qisa

        if self._backend in [
            BackendType.QUANTUM_SIM,
            BackendType.SYMQC,
            BackendType.ZUCHONGZHI,
            BackendType.TEUQILA,
        ]:
            return Qisa.QCIS

        if self._backend in [BackendType.QUANTIFY]:
            return Qisa.Quantify

        raise ValueError(f"Found unknown backend {self._backend}")

    @property
    def called_qu_dir(self):
        """The directory of the called Quingo file."""

        # use resolve() to handle relative path like `..`
        abs_called_qg_fn = Path(self.called_qu_fn).resolve()
        return abs_called_qg_fn.parent

    @property
    def include_dir(self):
        """
        Generate the include directories for the Quingo compiler.
        """
        _inc_dir = []
        _inc_dir.append(self.called_qu_dir)
        _inc_dir.append(self.build_dir)
        return _inc_dir
