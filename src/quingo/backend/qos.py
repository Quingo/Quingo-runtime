from __future__ import annotations
from numpy.typing import NDArray
from typing import List, Union
import json

from quingo.utils import ensure_path
from .backend_hub import BackendType
from .if_backend import If_backend
from quingo.core.exe_config import ExeMode, ExeConfig
from pyqos.experiment.data_taking.scan_circuits import RunCircuits


class QOS(If_backend):
    """A functional QCIS simulation backend using PyQCISim and QuantumSim."""

    def __init__(self):
        super().__init__(BackendType.QOS)

    def upload_program(self, prog_fn):
        """
        Upload assembly or binary program to the simulator.

        Args:
            prog_fn: the name of the assembly or binary file.
        """
        prog_fn = ensure_path(prog_fn)
        self.qcis_circuit = prog_fn.open("r").read()
        qubits_fn = prog_fn.parent / (prog_fn.stem + ".json")
        self.qubits = json.load(qubits_fn.open("r"))

    def execute(self, exe_config: ExeConfig) -> Union[List | NDArray]:
        """Execute the given quantum circuit.
        Args:
          - mode (str): the simulation mode to use:

        The number of shots is specified in exe_config.num_shots, which is only valid for
          ExeMode.SimShots.
        """
        if exe_config.mode == ExeMode.RealMachine:
            # print("qubits  = ", self.qubits)
            # print("qcis_circuit = ", self.qcis_circuit)
            # return "qqqqq"
            raw_res = RunCircuits(
                qubits=[self.qubits],
                use_template=False,
                circuits=([self.qcis_circuit] * exe_config.qos_circuit_times),
                data_type="P01",
                sampling_interval=200e-6,
                num_shots=exe_config.num_shots,
            )
            raw_res.wait()
            frams = raw_res.dataset.get_stream_data()
            return frams

        raise ValueError(
            "Unsupported execution mode ({}) for QOS.".format(exe_config.mode)
        )
