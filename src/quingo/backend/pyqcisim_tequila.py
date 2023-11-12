from .backend_hub import BackendType
from .if_backend import If_backend
from quingo.core.exe_config import *
from quingo.core.utils import *
from pyqcisim.simulator import PyQCISim

logger = get_logger((__name__).split(".")[-1])


class PyQCISim_tequila(If_backend):
    """A functional QCIS simulation backend using PyQCISim and Tequila."""

    def __init__(self):
        super().__init__(BackendType.TEUQILA)
        self.sim = PyQCISim()
        self.sim.setBackend("tequila")
        self.res = None

    def upload_program(self, prog_fn):
        prog_fn = ensure_path(prog_fn)

        program = prog_fn.open("r").read()
        self.sim.compile(program)

    def execute(self, exe_config: ExeConfig):
        if exe_config.mode == ExeMode.SimFinalResult:
            return self.sim.simulate("one_shot", exe_config.num_shots)

        raise ValueError(
            "Unsupported execution mode ({}) for TEQUILA.".format(exe_config.mode)
        )
