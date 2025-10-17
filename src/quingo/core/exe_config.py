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
        qcloud_platform_login_key: str = None,  # use for connecting XIAOHONG
        qcloud_machine_name: str = None,  # use for connecting XIAOHONG
        qos_circuit_times: int = 100,  # use for connecting QOS
        noise_config=None,
        enable_resource_estimation: bool = False,
    ):
        self.mode = mode
        self.num_shots = num_shots
        self.qcloud_platform_login_key = qcloud_platform_login_key
        self.qcloud_machine_name = qcloud_machine_name
        self.qos_circuit_times = qos_circuit_times
        self.noise_config = noise_config
        self.enable_resource_estimation = enable_resource_estimation

    def __str__(self) -> str:
        return str(self.mode)
