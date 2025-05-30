import enum


class ExeMode(enum.Enum):
    """
    Enumeration representing different result format.

    Attributes:
        SimFinalResult: for obtaining the final result.
        SimStateVector: Simulation mode for obtaining the state vector.
        SimMatrix: Simulation mode for obtaining the matrix representation.
        RealMachine: Mode for executing on a real quantum machine.
    """

    SimShots = enum.auto()
    SimFinalResult = enum.auto()
    SimStateVector = enum.auto()
    SymbolicStateVector = enum.auto()
    SimProbability = enum.auto()
    RealMachine = enum.auto()


class ExeConfig:
    def __init__(
        self,
        mode: ExeMode = ExeMode.SimShots,
        num_shots: int = 1,
        xh_login_key: str = None,  # use for connecting XIAOHONG
        xh_machine_name: str = None,  # use for connecting XIAOHONG
        quantacs_redis_host: str = None,  # use for connecting QUANTACS
        quantacs_redis_port: int = None,  # use for connecting QUANTACS
        quantacs_redis_db: int = 0,  # use for connecting QUANTACS
        quantacs_qubits: list = None,  # use for connecting QUANTACS
        quantacs_gate_decompose: bool = False,  # use for connecting QUANTACS
        qos_circuit_times: int = 100,  # use for connecting QOS
        noise_config=None,
    ):
        self.mode = mode
        self.num_shots = num_shots
        self.xh_login_key = xh_login_key
        self.xh_machine_name = xh_machine_name
        self.qos_circuit_times = qos_circuit_times
        self.noise_config = noise_config
        self.quantacs_redis_host = quantacs_redis_host
        self.quantacs_redis_port = quantacs_redis_port
        self.quantacs_redis_db = quantacs_redis_db
        self.quantacs_qubits = quantacs_qubits
        self.quantacs_gate_decompose = quantacs_gate_decompose

    def __str__(self) -> str:
        return str(self.mode)
