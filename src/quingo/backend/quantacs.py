from quingo.utils import ensure_path
from .backend_hub import BackendType
from .if_backend import If_backend
from quingo.core.exe_config import ExeConfig, ExeMode
# from quingo.lib.pyezQ import Account
import redis
import pickle
from quingo.lib.qcis_to_qasm import QcisToQasm





class QuantaCS(If_backend):
    def __init__(self):
        super().__init__(BackendType.QUANTACS)
        self.redis_client = None
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
        self.set_redis_client(exe_config.quantacs_redis_host, exe_config.quantacs_redis_port)
        qasm_code = QcisToQasm().convert_qcis_to_qasm(self.qcis_circuit)
        task_data = {
            "task_name": "quantacs_task",  # 可自定义唯一任务名
            "qasm": qasm_code,  # 生成的QCIS指令
            "qubits": exe_config.quantacs_qubits,  # 量子比特序列
            "num_repetition": exe_config.num_shots,  # 重复次数
            "gate_decompose": exe_config.quantacs_gate_decompose,
        }
        self.qubit_list = exe_config.quantacs_qubits

        # submit job
        print(f"Start execute:")
        print(f"num shots = {exe_config.num_shots}")
        msg = pickle.dumps(task_data)
        self.redis_client.lpush("task_manager", msg)

        RECV_TIMEOUT = 3600
        def get_out_queue_name(task_name: str) -> str:
            return f"{task_name}_output"
        def receive_msg_from_rds(task_name):
            name_out = get_out_queue_name(task_name)
            msg = self.redis_client.brpop(name_out, timeout=RECV_TIMEOUT)
            return msg

        # 获取结果
        result = receive_msg_from_rds(task_data["task_name"])
        if result is None:
            raise TimeoutError("等待测试机响应超时")
        # print(result)
        # 解析结果数据
        _, msg_bytes = result
        msg = pickle.loads(msg_bytes)
        print(f"Data from sc-devices: {msg}")
        if isinstance(msg, str) and "Traceback" in msg:
            print("error message from executor: ", msg)
            raise RuntimeError(f"{msg}")

        # read result
        result = self.format_result(msg)
        return result

    def set_redis_client(self, redis_host, redis_port):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=0,decode_responses=False)

    def format_result(self, result):
        origin_result = result[0]
        return {"qubits": self.qubit_list, "results": origin_result[2:]}
