from pathlib import Path
from statistics import mode
from quingo.if_backend.if_backend import If_backend
import quingo.global_config as gc
from quingo.core.utils import *
from dqcsim_quiets.frontend import QUIETs
from dqcsim.plugin import *
from dqcsim.host import *

logger = get_logger((__name__).split(".")[-1])


class IfDQCsim(If_backend):
    """A functional QUIETS simulation backend using Tequila."""

    def __init__(self, **kwargs):  # 关键字参数
        super().__init__("DQCsim_Tequila", is_simaultor=True)
        self.sim = Simulator(stderr_verbosity=Loglevel.INFO).with_backend("tequila")
        self.verbose = kwargs.pop("verbose", False)
        self.loglevel = kwargs.pop("loglevel", logging.INFO)
        logger.setLevel(self.loglevel)
        self.res = None

    def available(self):
        return True

    def get_qisa(self):
        return "quiet-s"

    def set_log_level(self, log_level):
        self.log_level = log_level
        logger.setLevel(self.log_level)

    def set_verbose(self, verbose):
        pass

    def upload_program(self, prog_fn, is_binary=False):
        """
        Upload assembly or binary program to the simulator.

        Args:
            prog_fn: the name of the assembly file.
            is_binary: True when the uploaded program is in binary format.
                       It should be False.
        """
        assert not is_binary

        if not isinstance(prog_fn, Path):
            prog_fn = Path(prog_fn)

        if not prog_fn.exists():
            quingo_err("Cannot find the assembly file: {}".format(prog_fn))
            return False

        try:
            frontend = QUIETs(prog_fn)
            self.sim.with_frontend(frontend)
            return True
        except Exception as e:
            quingo_err("Error in compiling the QCIS program using SymQC: {}".format(e))
            return False

    def execute(self):
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
        with self.sim as simulation:
            simulation.run()
            self.res = self.sim.recv()
        return True

    def read_result(self):
        """This function tries to read the computation result of the quantum kernel."""
        # we use below to get the res.
        # func_int = res["func_int"]
        # func_double = res["func_double"]
        # func_qubit = res["func_qubit"]
        # qubit_masure = res["qubit_masure"]
        # e.g. when we want to get the qubit q1 measure value:
        #   qubit_masure[func_qubit["q1"][0]]
        #   returns (measure value, probablity)
        return self.res
