from pathlib import Path
from quingo.if_backend.if_backend import If_backend
import quingo.global_config as gc
from quingo.core.utils import *
import time
import uuid
import ezQpy

logger = get_logger((__name__).split(".")[-1])


class Zuchongzhi(If_backend):

    def __init__(self, **kwargs):
        super().__init__("Zuchongzhi", is_simaultor=False)
        self.verbose = kwargs.pop("verbose", False)
        self.loglevel = kwargs.pop("loglevel", logging.INFO)
        logger.setLevel(self.loglevel)
        self.account = None
        self.lab_id = None
        self.exp_id = None
        self.query_id = None
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

        qcis_circuit = prog_fn.open("r").read()
        qcis_circuit = map_qubit(qcis_circuit)
        '''
        qcis_circuit = self.account.assign_parameters(
            circuit=qcis_circuit,
            parameters=None,
            values=None
        )
        '''
        exp_id = self.account.save_experiment(
            lab_id=self.lab_id,
            exp_data=qcis_circuit,
            version=str(uuid.uuid4())
        )
        if exp_id:
            self.exp_id = exp_id
            return True
        else:
            return False

    def execute(self, mode="one_shot", num_shots=1):
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
        query_id = self.account.run_experiment(
            exp_id=self.exp_id,
            num_shots=num_shots
        )
        if query_id:
            self.query_id = query_id
            return True
        else:
            return False

    def read_result(self):
        """This function tries to read the computation result of the quantum kernel."""
        res = self.account.query_experiment(
            query_id=self.query_id,
            max_wait_time=360000
        )
        if res:
            res = res["results"][1:]
            self.res = res
        return res

    def set_account(self, login_key, machine_name, lab_id=None):
        self.account = ezQpy.Account(login_key=login_key, machine_name=machine_name)
        if not lab_id:
            lab_name = time.strftime("%Y-%m-%d_%H-%M-%S")
            self.lab_id = self.account.create_experiment(lab_name)
        else:
            self.lab_id = lab_id

def map_qubit(qcis):
    qcis_list = qcis.split()
    qubit_map = {
        "Q1": "Q3",
        "Q2": "Q10",
        "Q3": "Q46",
        "Q4": "Q52",
        "Q5": "Q34",
        "Q6": "Q39",
        "Q7": "Q45",
        "Q8": "Q50",
        "Q9": "Q24",
        "Q10": "Q29",
        "Q11": "Q33",
        "Q12": "Q38"
    }
    for i, s in enumerate(qcis_list):
        if s in qubit_map.keys():
            qcis_list[i] = qubit_map[s]
        else:
            qcis_list[i] = "\n" + s
    qcis_mapped = " ".join(qcis_list)
    return qcis_mapped
