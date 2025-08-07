from datetime import datetime

from cqlib import TianYanPlatform

from quingo.core.exe_config import ExeConfig, ExeMode
from quingo.utils import ensure_path

from .backend_hub import BackendType
from .if_backend import If_backend


class ZDXLZ_Tianyan(If_backend):
    def __init__(self):
        super().__init__(BackendType.TIANYAN)
        self.ty_platform = None
        self.qcis_circuit = None

    def upload_program(self, prog_fn):
        """
        Upload assembly or binary program to the simulator.

        Args:
            prog_fn: the name of the assembly or binary file.
        """
        prog_fn = ensure_path(prog_fn)
        lines = []
        with prog_fn.open("r") as f:
            lines = f.readlines()

        if len(lines) == 0:
            raise ValueError("The program file is empty.")

        trimed_lines = []
        for line in lines:
            trimed_lines.append(" ".join(line.split()))

        self.qcis_circuit = "\n".join(
            [
                line.strip()
                for line in trimed_lines
                if line.strip() and not line.startswith("#")
            ]
        )
        # self.qcis_circuit = prog_fn.open("r").read()

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
                f"Unsupported execution mode ({exe_config.mode}) for Tianyan."
            )

        # connect Tianyan
        self.configure_platform(
            exe_config.qcloud_platform_login_key, exe_config.qcloud_machine_name
        )

        # submit job
        print(f"\n===================== Start execute: ===================== ")

        print("circuit:\n", self.qcis_circuit, sep="")
        print(
            "type of circuit:",
            type(self.qcis_circuit),
            " length:",
            len(self.qcis_circuit),
        )
        print("machine name:", exe_config.qcloud_machine_name)
        print(f"num shots = {exe_config.num_shots}")

        print("")

        query_id = self.ty_platform.submit_job(
            circuit=self.qcis_circuit,
            exp_name=f'quingo_exp.{datetime.now().strftime("%Y%m%d%H%M%S")}',
            num_shots=exe_config.num_shots,
        )

        # invalid query
        if not query_id:
            raise EnvironmentError("Fail to connect Tianyan!")

        # read result
        result = self.ty_platform.query_experiment(
            query_id=query_id, max_wait_time=3600, sleep_time=5
        )
        result = self.format_result(result)
        return result

    def configure_platform(self, login_key, machine_name):
        self.ty_platform = TianYanPlatform(login_key=login_key)
        print(f"Set account successfully:")
        print(f"   login key = {login_key[0:5]}" + "*" * (len(login_key) - 5))
        self.ty_platform.set_machine(machine_name)
        print(f"   machine name = {machine_name}")

    def format_result(self, result):
        print("result:", result)
        # origin_result = result[0]["results"]
        # return {"qubits": origin_result[0], "results": origin_result[1:]}
