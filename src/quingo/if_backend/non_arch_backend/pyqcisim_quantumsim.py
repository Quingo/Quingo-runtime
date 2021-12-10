from pathlib import Path
from quingo.if_backend.if_backend import If_backend
import quingo.global_config as gc
from quingo.core.utils import *
from pyqcisim.simulator import PyQCISim

logger = get_logger((__name__).split('.')[-1])


class PyQCISim_quantumsim(If_backend):
    """A functional QCIS simulation backend using PyQCISim and QuantumSim."""

    def __init__(self, **kwargs):
        super().__init__("PyQCISim_QuantumSim", is_simaultor=True)
        self.sim = PyQCISim()
        self.pyqcisim_dir = gc.qgrtsys_root_dir / "if_backend" / "pyqcisim"
        self.verbose = kwargs.pop('verbose', False)
        self.loglevel = kwargs.pop('loglevel', logging.INFO)
        logger.setLevel(self.loglevel)
        self.res = None

    def available(self):
        return True

    def get_qisa(self):
        return "qcis"

    def set_log_level(self, log_level):
        self.log_level = log_level
        logger.setLevel(self.log_level)

    def set_verbose(self, verbose):
        pass

    def upload_program(self, prog_fn, is_binary=False):
        """
        Upload assembly or binary program to the simulator.

        Args:
            prog_fn: the name of the assembly or binary file.
            is_binary: True when the uploaded program is in binary format.
        """
        assert not is_binary

        if not isinstance(prog_fn, Path):
            prog_fn = Path(prog_fn)

        f = prog_fn.open('r').read()
        try:
            self.sim.compile(f)
            return True
        except Exception as e:
            quingo_err("Error in the QCIS program compiling process of PyQCISim: {}".format(e))
            return False

    def execute(self, mode="one_shot", num_shots=1):
        '''Execute the given quantum circuit.
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
        '''
        try:
            if mode == 'state_vector':  # mapping between the name of simulation modes
                raw_res = self.sim.simulate('final_state')
                self.res = raw_res['quantum'][1]
            else:
                self.res = self.sim.simulate(mode, num_shots)
            return True
        except Exception as e:
            quingo_err("Error in PyQCISim Simulation: {}".format(e))
            return False

    def read_result(self):
        """This function tries to read the computation result of the quantum kernel."""
        return self.res
