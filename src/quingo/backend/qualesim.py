from __future__ import annotations
from typing import Union
from quingo.utils import ensure_path
from pathlib import Path
from quingo.backend.backend_hub import BackendType
from quingo.backend.if_backend import If_backend
from quingo.core.exe_config import ExeConfig, ExeMode
import numpy as np


class QuaLeSim_base(If_backend):

    def __init__(self, backend_type=BackendType.QUALESIM_QUANTUMSIM):
        super().__init__(backend_type)
        from qualesim.plugin import Loglevel
        from qualesim.host import Simulator

        self.sim = Simulator(stderr_verbosity=Loglevel.OFF)
        if backend_type == BackendType.QUALESIM_QUANTUMSIM:
            self.sim.with_backend("quantumsim", verbosity=Loglevel.OFF)
        elif backend_type == BackendType.QUALESIM_TEQUILA:
            self.sim.with_backend("tequila", verbosity=Loglevel.OFF)
        else:
            raise ValueError(
                "The QuaLeSim backend only supports QUALESIM_QUANTUMSIM and QUALESIM_TEQUILA."
            )

        self.res = None

    def upload_program(self, prog_fn: Union[Path | str]):
        prog_fn = ensure_path(prog_fn)

        if prog_fn.suffix in [".qcis", ".qi"]:
            from qualesim.plugin import Loglevel

            self.sim.with_frontend(str(prog_fn), verbosity=Loglevel.OFF)
        else:
            raise TypeError(
                "found unsupported file suffix ({}). Currently supported are "
                "'.qcis' (for QCIS) and '.qi' (for QUIET-s)".format(prog_fn.suffix)
            )

    def upload_program_str(self, program: str):
        pass

    def execute(self, exe_config: ExeConfig):
        if exe_config.mode == ExeMode.SimShots:
            measure_mod = "one_shot"
            try:
                self.sim.simulate()
                res = self.sim.run(
                    measure_mod=measure_mod, num_shots=exe_config.num_shots
                )
                self.sim.stop()

                final_state = res["res"]
                final_state["quantum"] = tuple(final_state["quantum"])
                result = final_state["quantum"]

                return result

            except Exception as e:
                raise ValueError(
                    "error in QuaLeSim simulation with mode ({}): {}".format(
                        exe_config.mode, e
                    )
                )

        if exe_config.mode == ExeMode.SimFinalResult:
            measure_mod = "state_vector"
            try:
                self.sim.simulate()
                res = self.sim.run(measure_mod=measure_mod)
                self.sim.stop()
                final_state = eval(res["res"])
                result = dict()
                result["classical"] = final_state["classical"]
                result["quantum"] = tuple(
                    (final_state["quantum"][0], np.array(final_state["quantum"][1]))
                )
                return result

            except Exception as e:
                raise ValueError(
                    "error in QuaLeSim simulation with mode ({}): {}".format(
                        exe_config.mode, e
                    )
                )

        if exe_config.mode == ExeMode.SimStateVector:
            measure_mod = "state_vector"
            try:
                self.sim.simulate()
                res = self.sim.run(measure_mod=measure_mod)
                self.sim.stop()
                final_state = eval(res["res"])
                return final_state["quantum"]

            except Exception as e:
                raise ValueError(
                    "error in QuaLeSim simulation with mode ({}): {}".format(
                        exe_config.mode, e
                    )
                )

        raise ValueError(
            "Unsupported execution mode ({}) for QuaLeSim_QuantumSim.".format(
                exe_config.mode
            )
        )


class QuaLeSim_tequila(QuaLeSim_base):
    def __init__(self):
        super().__init__(BackendType.QUALESIM_TEQUILA)


class QuaLeSim_quantumsim(QuaLeSim_base):
    def __init__(self):
        super().__init__(BackendType.QUALESIM_QUANTUMSIM)
