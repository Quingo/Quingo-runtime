from quingo.core.exe_config import ExeConfig, ExeMode
from quingo.lib.pyezQ import Account
from quingo.utils import ensure_path

from .backend_hub import BackendType
from .if_backend import If_backend


class XiaoHong(If_backend):
    def __init__(self):
        super().__init__(BackendType.XIAOHONG)
        self.account = None
        self.qcis_circuit = None

    def upload_program(self, prog_fn):
        """
        Upload assembly or binary program to the simulator.

        Args:
            prog_fn: the name of the assembly or binary file.
        """
        prog_fn = ensure_path(prog_fn)
        self.qcis_circuit = prog_fn.open("r").read()

    def upload_program_str(self, program: str):
        """upload the program string to the simulator."""
        self.qcis_circuit = program

    def execute(self, exe_config: ExeConfig):
        """Execute the given quantum circuit.
        Args:
          - mode (str): the simulation mode to use:
              - "one_shot": the simulation result is a dictionary with each key being a qubit
                  measured, and the value is the outcome of measuring this qubit.
          - num_shots (int): the number of iterations performed in `one_shot` mode.
          - xh_login_key (str): login key to connect XiaoHong
          - xh_machine_name (str): name of machine name to execute qcis
        """
        if not exe_config.mode == ExeMode.RealMachine:
            raise ValueError(
                f"Unsupported execution mode ({exe_config.mode}) for XiaoHong."
            )

        # connect XiaoHong
        self.set_account(
            exe_config.qcloud_platform_login_key, exe_config.qcloud_machine_name
        )

        # submit job
        print(f"Start execute:")
        print(f"num shots = {exe_config.num_shots}")
        query_id = self.account.submit_job(
            self.qcis_circuit, num_shots=exe_config.num_shots
        )

        # invalid query
        if not query_id:
            raise EnvironmentError("Fail to connect XiaoHong!")

        # read result
        result = self.account.query_experiment(query_id, max_wait_time=360000)
        result = self.format_result(result)
        return result

    def set_account(self, login_key, machine_name):
        self.account = Account(login_key=login_key, machine_name=machine_name)
        print(f"Set account successfully:")
        print(f"   login key = {login_key[0:5]}" + "*" * (len(login_key) - 5))
        print(f"   machine name = {machine_name}")

    def format_result(self, result):
        origin_result = result[0]["results"]
        return {"qubits": origin_result[0], "results": origin_result[1:]}
