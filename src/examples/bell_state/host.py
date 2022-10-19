import logging
from quingo import quingo_interface as qi
from pathlib import Path

qi.set_verbose(True)
qi.set_log_level(logging.DEBUG)
qi.set_compiler("mlir")

# if qi.connect_backend("pyqcisim_quantumsim") is False:
if qi.connect_backend("symqc") is False:
    exit(-1)

qu_file = Path(__file__).parent / "kernel.qu"


def routine(circ_name, num_shots=1):
    qi.set_num_shots(num_shots)
    if not qi.call_quingo(qu_file, circ_name):
        print("Failed to call {}".format(circ_name))
    print("The result of {} is:".format(circ_name))
    print(qi.read_result())


routine("bell_state", 10)
