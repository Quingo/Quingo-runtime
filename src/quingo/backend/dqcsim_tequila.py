from .backend_hub import BackendType
from .if_backend import If_backend
from quingo.core.exe_config import *
from quingo.core.utils import *
from dqcsim.plugin import *
from dqcsim.host import *

logger = get_logger((__name__).split(".")[-1])


def bitwise_reverse_sort(lst, k):
    sorted_lst = []
    for i in range(len(lst)):
        sorted_lst.append(lst[int("0b" + bin(i)[2:].zfill(k)[::-1], 2)])
    return sorted_lst


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
            try:
                self.sim.simulate()
                res = self.sim.run(
                    measure_mod=measure_mod, num_shots=exe_config.num_shots
                )
                self.sim.stop()
                final_state = res["res"]
                final_state["quantum"] = tuple(final_state["quantum"])
                return final_state["quantum"]
            except:
                raise ValueError(
                    "Here is some wrong with ({}) for DQCSIM_TEQUILA.".format(
                        exe_config.mode
                    )
                )

        if exe_config.mode == ExeMode.SimStateVector:
            measure_mod = "state_vector"
            try:
                self.sim.simulate()
                res = self.sim.run(measure_mod=measure_mod)
                self.sim.stop()
                final_state = eval(res["res"])
                qu = bitwise_reverse_sort(
                    final_state["quantum"][1], len(final_state["quantum"][0])
                )
                final_state["quantum"] = (final_state["quantum"][0], qu)
                return final_state
            except:
                raise ValueError(
                    "Here is some wrong with ({}) for DQCSIM_TEQUILA.".format(
                        exe_config.mode
                    )
                )

        raise ValueError(
            "Unsupported execution mode ({}) for DQCSIM_TEQUILA.".format(
                exe_config.mode
            )
        )
