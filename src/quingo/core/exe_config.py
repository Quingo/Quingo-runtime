import enum


class ExeMode(enum.Enum):
    SimFinalResult = enum.auto()
    SimStateVector = enum.auto()
    SimMatrix = enum.auto()
    RealMachine = enum.auto()


def is_simulation(exe_mode):
    return exe_mode in [
        ExeMode.SimFinalResult,
        ExeMode.SimStateVector,
        ExeMode.SimMatrix,
    ]


class ExeConfig:
    def __init__(
        self,
        mode: ExeMode = ExeMode.SimFinalResult,
        num_shots: int = 1,
        xh_login_key: str = None,  # use for connecting XIAOHONG
        xh_machine_name: str = None,  # use for connecting XIAOHONG
    ):
        self.mode = mode
        self.num_shots = num_shots
        self.xh_login_key = xh_login_key
        self.xh_machine_name = xh_machine_name

    def __str__(self) -> str:
        return str(self.mode)
