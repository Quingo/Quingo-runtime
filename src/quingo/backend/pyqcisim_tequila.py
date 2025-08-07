from quingo.utils import ensure_path
from .backend_hub import BackendType
from .if_backend import If_backend
from quingo.core.exe_config import ExeConfig, ExeMode
from pyqcisim.simulator import PyQCISim
import numpy as np


class PyQCISim_tequila(If_backend):
    """A functional QCIS simulation backend using PyQCISim and Tequila."""

    def __init__(self):
        super().__init__(BackendType.TEQUILA)
        self.sim = PyQCISim()
        self.sim.setBackend("tequila")
        self.res = None

    def upload_program(self, prog_fn):
        prog_fn = ensure_path(prog_fn)

        program = prog_fn.open("r").read()
        self.sim.compile(program)

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
            return self.sim.simulate(
                "one_shot", exe_config.num_shots, noise_config=exe_config.noise_config
            )

        if exe_config.mode == ExeMode.SimFinalResult:
            return self.sim.simulate(
                "final_result", noise_config=exe_config.noise_config
            )

        if exe_config.mode == ExeMode.SimStateVector:
            names, nd_array_values = self.sim.simulate(
                "state_vector", noise_config=exe_config.noise_config
            )
            return (names, nd_array_values)

        if exe_config.mode == ExeMode.SimProbability:
            return self.sim.simulate(
                "probability", noise_config=exe_config.noise_config
            )

        raise ValueError(
            "Unsupported execution mode ({}) for TEQUILA.".format(exe_config.mode)
        )
