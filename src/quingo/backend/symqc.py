from quingo.utils import ensure_path
from .backend_hub import BackendType
from .if_backend import If_backend
from quingo.core.exe_config import ExeConfig, ExeMode
from symqc.simulator import SymQC
import numpy as np


class IfSymQC(If_backend):
    """A functional QCIS simulation backend based on symbolic computation."""

    def __init__(self):
        super().__init__(BackendType.SYMQC)
        self.sim = SymQC()

    def upload_program(self, prog_fn):
        """
        Upload assembly or binary program to the simulator.

        Args:
            prog_fn: the name of the assembly file.
        """
        prog_fn = ensure_path(prog_fn)
        if str(prog_fn).endswith(".qcis"):
            self.sim.compile_file(prog_fn)
        else:
            raise TypeError("The SymQC simulator can only accept QCIS instructions.")

    def upload_program_str(self, program: str):
        """upload the program string to the simulator."""
        self.sim.compile(program)

    def execute(self, exe_config: ExeConfig):
        """Execute the given quantum circuit.
        Args:
          - exe_config (ExeConfig): the configuration used to perform simulation by SymQC.

        The number of shots is specified in exe_config.num_shots, which is only valid for
          ExeMode.SimShots.
        """
        if exe_config.mode == ExeMode.SimShots:
            return self.sim.simulate("one_shot", exe_config.num_shots)

        if exe_config.mode == ExeMode.SimFinalResult:
            raw_res = self.sim.simulate("final_state")
            raw_res["quantum"] = (
                raw_res["quantum"][0],
                np.array(raw_res["quantum"][1]).reshape(
                    -1,
                ),
            )
            return raw_res

        if exe_config.mode == ExeMode.SimStateVector:
            raw_res = self.sim.simulate("final_state")
            return raw_res["quantum"]

        raise ValueError(
            "Unsupported execution mode ({}) for symqc.".format(exe_config.mode)
        )
