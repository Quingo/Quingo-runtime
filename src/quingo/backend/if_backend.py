from .backend_hub import BackendType, Backend_hub
from quingo.core.exe_config import ExeConfig


class If_backend:
    """The interface class for Quingo backends.

    Any backend should inherit from this interface.
    """

    def __init__(self, be_type: BackendType):
        self._be_type = be_type

    def get_type(self):
        return self._be_type

    def get_qisa(self):
        return Backend_hub().get_qisa(self._be_type)

    def is_simulator(self):
        return Backend_hub().is_simulator(self._be_type)

    def upload_program(self, program):
        raise NotImplementedError

    def upload_program_str(self, program: str):
        raise NotImplementedError

    def execute(self, exe_config: ExeConfig):
        raise NotImplementedError
