import logging
from quingo import quingo_interface as qi
from pathlib import Path

qi.connect_backend('pyqcisim_quantumsim')

qu_file = Path(__file__).parent / "kernel.qu"

def routine(circ_name, num_shots=1, num_qubits=1):
    qi.set_num_shots(num_shots)
    qi.call_quingo(qu_file, circ_name, num_qubits)
    print("The result of {} is:".format(circ_name))
    print(qi.read_result())


routine("ghz", 5, 4)
