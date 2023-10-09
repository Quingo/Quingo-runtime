import importlib
import enum
from .qisa import Qisa


class BackendType(enum.Enum):
    SYMQC = enum.auto()
    QUANTIFY = enum.auto()
    ZUCHONGZHI = enum.auto()
    DQCSIM_TEQUILA = enum.auto()
    DQCSIM_QUANTUMSIM = enum.auto()


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner


@singleton
class Backend_hub:
    def __init__(self):
        self.backends = {
            BackendType.QUANTIFY: (
                "quantify",
                "to be added the hardware driver",
                False,
                Qisa.Quantify,
            ),
            BackendType.SYMQC: (
                "IfSymQC",
                "symqc",
                True,
                Qisa.QCIS,
            ),
            BackendType.ZUCHONGZHI: (
                "Zuchongzhi",
                "zuchongzhi",
                False,
                Qisa.QCIS,
            ),
            BackendType.DQCSIM_TEQUILA: (
                "DQCsim_tequila",
                "dqcsim_tequila",
                True,
                Qisa.QCIS,
            ),
            BackendType.DQCSIM_QUANTUMSIM: (
                "DQCsim_quantumsim",
                "dqcsim_quantumsim",
                True,
                Qisa.QCIS,
            ),
        }

    def support(self, backend_type):
        return backend_type in self.backends

    def import_be_module(self, module_path):
        """import the backend module based on the module_path.

        The module is imported here because the backend module may not be installed.
        We only import the module when it is needed.
        """
        prefix = "quingo.backend."
        full_module_path = prefix + module_path
        module = importlib.import_module(full_module_path)
        return module

    def is_simulator(self, backend_type):
        be_class_name, module_path, is_sim, qisa = self.backends[backend_type]
        return is_sim

    def get_qisa(self, backend_type):
        be_class_name, module_path, is_sim, qisa = self.backends[backend_type]
        return qisa

    def get_instance(self, backend_type):
        be_class_name, module_path, is_sim, qisa = self.backends[backend_type]
        return getattr(self.import_be_module(module_path), be_class_name)()