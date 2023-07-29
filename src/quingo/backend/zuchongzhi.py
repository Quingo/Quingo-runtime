import time, uuid, os
from .backend_hub import BackendType
from .if_backend import If_backend
from quingo.core.exe_config import *
from quingo.core.utils import *
import ezQpy


logger = get_logger((__name__).split(".")[-1])


class Zuchongzhi(If_backend):
    def __init__(self):
        super().__init__(BackendType.ZUCHONGZHI)
        self.account = None
        self.lab_id = None
        self.exp_id = None
        self.query_id = None
        self.res = None

    def upload_program(self, prog_fn):
        """
        Upload assembly or binary program to the simulator.

        Args:
            prog_fn: the name of the assembly or binary file.
        """
        prog_fn = ensure_path(prog_fn)

        qcis_circuit = prog_fn.open("r").read()
        logger.info("circuit before mapping{}{}".format(os.linesep, qcis_circuit))
        qcis_circuit = map_qubit(qcis_circuit)
        logger.info("circuit after mapping{}{}".format(os.linesep, qcis_circuit))
        """
        qcis_circuit = self.account.assign_parameters(
            circuit=qcis_circuit,
            parameters=None,
            values=None
        )
        """
        exp_id = self.account.save_experiment(
            lab_id=self.lab_id, exp_data=qcis_circuit, version=str(uuid.uuid4())
        )
        if exp_id:
            self.exp_id = exp_id
            return True
        else:
            return False

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
        if exe_config.mode == ExeMode.SimFinalResult:
            query_id = self.account.run_experiment(
                exp_id=self.exp_id, num_shots=exe_config.num_shots
            )
            res = self.account.query_experiment(query_id, max_wait_time=360000)
            res = res["results"][1:]
            return res

        raise ValueError(
            "Unsupported execution mode ({}) for Zuchongzhi.".format(exe_config.mode)
        )

    def set_account(self, login_key, machine_name, lab_id=None):
        self.account = ezQpy.Account(login_key=login_key, machine_name=machine_name)
        if not lab_id:
            lab_name = time.strftime("%Y-%m-%d_%H-%M-%S")
            self.lab_id = self.account.create_experiment(lab_name)
        else:
            self.lab_id = lab_id


def map_qubit(qcis):
    qubit_map = {
        "Q1": "Q3",
        "Q2": "Q9",
        "Q3": "Q46",
        "Q4": "Q52",
        "Q5": "Q34",
        "Q6": "Q39",
        "Q7": "Q45",
        "Q8": "Q50",
        "Q9": "Q24",
        "Q10": "Q29",
        "Q11": "Q33",
        "Q12": "Q38",
    }
    map_line = lambda line: " ".join(qubit_map.get(s, s) for s in line.split())
    return os.linesep.join(map_line(line) for line in qcis.strip().split(os.linesep))
