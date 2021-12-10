import logging
from quingo import if_quingo
from pathlib import Path

if_quingo.set_verbose(True)
if_quingo.set_log_level(logging.DEBUG)
if_quingo.set_compiler('mlir')

if if_quingo.connect_backend('pyqcisim_quantumsim') is False:
    print("cannot connect to pyqcisim_quantumsim")
    exit(-1)

cur_dir = Path(__file__).parent
qu_file = cur_dir / "kernel.qu"


def routine(circ_name, num_shots=1):
    if_quingo.set_num_shots(num_shots)
    if not if_quingo.call_quingo(qu_file, circ_name):
        print("Failed to call {}".format(circ_name))
    print("The result of {} is:".format(circ_name))
    print(if_quingo.read_result())


routine("bell_state", 1000)
