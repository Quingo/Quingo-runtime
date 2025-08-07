from __future__ import annotations
from numpy.typing import NDArray
from typing import List, Union


from quingo.utils import ensure_path
from .backend_hub import BackendType
from .if_backend import If_backend
from quingo.core.exe_config import ExeMode, ExeConfig
from pyqcisim.simulator import PyQCISim


class PyQCISim_quantumsim(If_backend):
    """A functional QCIS simulation backend using PyQCISim and QuantumSim."""

    def __init__(self):
        super().__init__(BackendType.QUANTUM_SIM)
        self.sim = PyQCISim()

    def upload_program(self, prog_fn):
        """
        Upload assembly or binary program to the simulator.

        Args:
            prog_fn: the name of the assembly or binary file.
        """
        prog_fn = ensure_path(prog_fn)

        program = prog_fn.open("r").read()
        self.sim.compile(program)

    def upload_program_str(self, program: str):
        """upload the program string to the simulator."""
        self.sim.compile(program)

    def execute(self, exe_config: ExeConfig) -> Union[List | NDArray]:
        """Execute the given quantum circuit.
        Args:
          - mode (str): the simulation mode to use:

        The number of shots is specified in exe_config.num_shots, which is only valid for
          ExeMode.SimShots.
        """
        if exe_config.mode == ExeMode.SimShots:
            raw_res = self.sim.simulate("one_shot", exe_config.num_shots)
            return raw_res

        if exe_config.mode == ExeMode.SimFinalResult:
            raw_res = self.sim.simulate("final_result")
            return raw_res

        if exe_config.mode == ExeMode.SimStateVector:
            raw_res = self.sim.simulate("state_vector")
            return raw_res

        raise ValueError(
            "Unsupported execution mode ({}) for quantumsim.".format(exe_config.mode)
        )
