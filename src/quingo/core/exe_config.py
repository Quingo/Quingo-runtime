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
    RealMachine = enum.auto()


class ExeConfig:
    def __init__(
        self,
        mode: ExeMode = ExeMode.SimShots,
        num_shots: int = 1,
        xh_login_key: str = None,  # use for connecting XIAOHONG
        xh_machine_name: str = None,  # use for connecting XIAOHONG
        qos_circuit_times: int = 100,  # use for connecting QOS
        noise_config=None,
    ):
        self.mode = mode
        self.num_shots = num_shots
        self.xh_login_key = xh_login_key
        self.xh_machine_name = xh_machine_name
        self.qos_circuit_times = qos_circuit_times
        self.noise_config = noise_config

    def __str__(self) -> str:
        return str(self.mode)
