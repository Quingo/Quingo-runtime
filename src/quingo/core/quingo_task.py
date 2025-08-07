from pathlib import Path
import shutil
import quingo.global_config as gc
import tempfile
from quingo.backend.backend_hub import BackendType
from quingo.backend.qisa import Qisa
from quingo.utils import ensure_path
import time
import os

DEBUG_MODE = False


def create_empty_dir(dir_path: Path):
    if dir_path.exists():
        shutil.rmtree(str(dir_path))
    dir_path.mkdir()


def get_cur_time_as_str():
    cur_time = time.localtime()
    return "{:04}{:02}{:02}_{:02}{:02}{:02}".format(
        cur_time.tm_year,
        cur_time.tm_mon,
        cur_time.tm_mday,
        cur_time.tm_hour,
        cur_time.tm_min,
        cur_time.tm_sec,
    )


class Quingo_task:
    def __init__(
        self,
        called_qu_fn: Path,
        called_func: str,
        build_under=None,
        debug_mode=False,
        delete_build_dir=True,
        qisa=None,
        backend=BackendType.QUANTUM_SIM,
        qubits_info=None,
    ) -> None:
        """
        Initializes a Quingo task object.

        This constructor defines a Quingo task by specifying the Quingo file and the entry function. It stores essential information required for executing the Quingo task, including paths, debug mode, target qisa, and backend. Other properties are calculated on-demand to minimize stored information and reduce inconsistency risks.

        Parameters:
        - called_qu_fn (Path): The path of the Quingo file to be called.
        - called_func (str): The name of the entry function within the Quingo file.
        - build_under (Optional[Path]): The path under which the build directory should be created.
            If None, the build directory's location is determined based on the debug mode.
        - debug_mode (bool): If True, the task runs in debug mode, affecting the location of the
            build directory and possibly other behaviors.
        - delete_build_dir (bool): delete the build directory after task is completed.
            Defaults to True
        - qisa (Optional[Any]): The target assembly specification.
        - backend (BackendType): The target backend for the Quingo task. Defaults to QuantumSim.
        - qubits_info (Optional[Any]): Information about the qubits used in the task.

        Note:
        The `build_dir` is calculated the first time it is needed.
        In debug mode, it is located in the `build` dir under the current working directory.
        Otherwise, it is a temporary directory (like `/tmp/`).
        """
        # file name and function name
        called_qu_fn = ensure_path(called_qu_fn)
        self._called_qu_fn = called_qu_fn
        self._called_func = called_func

        self.debug_mode = debug_mode

        # qisa and backend
        self._qisa = qisa
        self._backend = backend
        self._qubits_info = qubits_info

        self.create_build_dir(build_under, delete_build_dir, debug_mode)

    def create_build_dir(
        self, build_under=None, delete_build_dir=True, debug_mode=False
    ):
        """It specifies a temporary build directory for this task.
        By default, this build directory will be deleted when the task is destroyed.

        When `build_under` is None, the build directory is under system temporary directory.
        Otherwise, a new build directory will be created under this given directory.

        When `debug_mode` is True, and `build_under` is None, a build directory will be created under `<cwd>/build/`.

        中文版需求说明：
          - 每个task对应一个build文件夹，还是每个task的每次执行对应一个文件夹？
            - 每个task对应一个文件夹
            - 如果一个task要进行多次执行，目前直接覆盖

          - 用户应当可以指定build文件夹的位置。
            - 使用特定的位置：在指定文件夹下创建临时文件夹
            - 若没有指定，则使用/tmp/。使用tmp时，该文件夹被使用完之后，会被删除

          - 文件夹用完之后默认被删除，但在用户指定下，临时文件夹用完之后可以被保留
        """
        if debug_mode and build_under is None:
            self.parent_work_dir = Path.cwd() / gc.build_dirname
        else:
            self.parent_work_dir = build_under

        self.delete_build_dir = False if debug_mode else delete_build_dir
        build_dir_prefix = "qg-" + get_cur_time_as_str() + "-"

        if self.parent_work_dir is not None:
            if not self.parent_work_dir.exists():
                self.parent_work_dir.mkdir()

        self.working_dir = tempfile.mkdtemp(
            dir=self.parent_work_dir,
            prefix=build_dir_prefix,
        )

        assert Path(self.working_dir).exists()

    def __del__(self):
        if self.delete_build_dir:
            shutil.rmtree(str(self.working_dir))

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
        """The path of the build directory. see `create_build_dir` for more details."""
        return Path(self.working_dir).absolute()

    @property
    def qisa_type(self):
        """
        Infer the qisa type from the selected backend.
        """
        if self._qisa is not None:
            return self._qisa

        if self._backend in [
            BackendType.QUANTUM_SIM,
            BackendType.TEQUILA,
            BackendType.SYMQC,
            BackendType.XIAOHONG,
            BackendType.QUALESIM_QUANTUMSIM,
            BackendType.QUALESIM_TEQUILA,
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
