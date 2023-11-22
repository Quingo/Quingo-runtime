from .backend_hub import BackendType
from .if_backend import If_backend
from quingo.core.exe_config import *
from quingo.core.utils import *
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

    def execute(self, exe_config: ExeConfig):
        """Execute the given quantum circuit.
        Args:
          - mode (str): the simulation mode to use:
              - "one_shot": the simulation result is a dictionary with each key being a qubit
                  measured, and the value is the outcome of measuring this qubit.
              - "final_state": the simulation result is a two-level dictionary:
                  {
                    'classical': {'Q1': 1, 'Q2': 0},
                    'quantum': (['Q3', 'Q4'], array([0, 1, 0, 0]))
                  }
          - num_shots (int): the number of iterations performed in `one_shot` mode.
        """
        if exe_config.mode == ExeMode.SimStateVector:
            raw_res = self.sim.simulate("final_state")
            return raw_res["quantum"][1]

        if exe_config.mode == ExeMode.SimFinalResult:
            return self.sim.simulate("one_shot", exe_config.num_shots)

        raise ValueError(
            "Unsupported execution mode ({}) for quantumsim.".format(exe_config.mode)
        )
