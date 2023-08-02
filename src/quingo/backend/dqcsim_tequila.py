from .backend_hub import BackendType
from .if_backend import If_backend
from quingo.core.exe_config import *
from quingo.core.utils import *
from dqcsim.plugin import *
from dqcsim.host import *

logger = get_logger((__name__).split(".")[-1])


class DQCsim_tequila(If_backend):
    """A functional QCIS simulation backend using PyQCISim and Tequila."""

    def __init__(self):
        super().__init__(BackendType.DQCSIM_TEQUILA)
        self.sim = Simulator(stderr_verbosity=Loglevel.OFF)
        self.sim.with_backend("tequila", verbosity=Loglevel.OFF)
        self.res = None

    def upload_program(self, prog_fn):
        prog_fn = ensure_path(prog_fn)
        self.sim.with_frontend(str(prog_fn), verbosity=Loglevel.OFF)

    def execute(self, exe_config: ExeConfig):
        if exe_config.mode == ExeMode.SimFinalResult:
            measure_mod = "one_shot"
            self.sim.simulate()
            res = self.sim.run(measure_mod=measure_mod, num_shots=exe_config.num_shots)
            self.sim.stop()
            final_state = res["final_state"]
            final_state["quantum"] = tuple(final_state["quantum"])
            return final_state

        raise ValueError(
            "Unsupported execution mode ({}) for DQCSIM_TEQUILA.".format(
                exe_config.mode
            )
        )
