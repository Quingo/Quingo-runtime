from pathlib import Path
from quingo import *


class Ansatz_circuit:
    def __init__(self, qu_file: Path, circ_name: str, num_params: int):
        self.qu_file = qu_file
        self.circ_name = circ_name
        self.num_params = num_params
        self._params = None
        self.backend = BackendType.QUANTUM_SIM
        self.exe_config = ExeConfig(ExeMode.SimStateVector)
        self.config_file = ""

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, params):
        if len(params) != self.num_params:
            raise ValueError(
                "The number of parameters ({}) does not match the number of parameters in the circuit ({})".format(
                    len(params), self.num_params
                )
            )
        self._params = params

    def with_params(self, params):
        self.params = params

    def with_backend(self, backend):
        self.backend = backend

    def with_config_file(self, config_file):
        self.config_file = config_file

    def get_ansatz(self):
        task = Quingo_task(self.qu_file, self.circ_name, debug_mode=False)
        qasm_fn = compile(task, params=self.params, config_file=self.config_file)
        res = execute(qasm_fn, self.backend, ExeConfig(ExeMode.SimStateVector))
        return res


# # get ansatz.
# def get_ansatz(circ: Ansatz_circuit, backend, config_file=""):
#     task = Quingo_task(circ.qu_file, circ.circ_name, debug_mode=False)
#     qasm_fn = compile(task, params=circ.params, config_file=config_file)
#     res = execute(qasm_fn, backend, ExeConfig(ExeMode.SimStateVector))
#     return res["quantum"][1]
