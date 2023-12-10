from .backend_hub import BackendType
from .if_backend import If_backend
from quingo.core.exe_config import *
from quingo.core.utils import *
from symqc.simulator import SymQC


logger = get_logger((__name__).split(".")[-1])


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
            return raw_res

        if exe_config.mode == ExeMode.SimFinalResult:
            return self.sim.simulate("one_shot", exe_config.num_shots)

        if exe_config.mode == ExeMode.SimMatrix:
            raise NotImplementedError(
                "Runtime has not supported SimMatrix with SymQC yet."
            )

        raise ValueError(
            "Unsupported execution mode ({}) for symqc.".format(exe_config.mode)
        )
