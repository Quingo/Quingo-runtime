import logging
from quingo import quingo_interface as qi
from pathlib import Path

if qi.connect_backend('pyqcisim_quantumsim') is False:
    exit(-1)

qu_file = Path(__file__).parent / "kernel.qu"


def routine(circ_name, num_shots=1, num_qubits=1):
    qi.set_num_shots(num_shots)
    if not qi.call_quingo(qu_file, circ_name, num_qubits):
        print("Failed to call {}".format(circ_name))
    print("The result of {} is:".format(circ_name))
    print(qi.read_result())


routine("ghz", 5, 4)
