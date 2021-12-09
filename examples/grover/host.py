import logging
from qgrtsys import if_quingo
from pathlib import Path

if_quingo.set_compiler("mlir")
if_quingo.connect_backend("pyqcisim_quantumsim")
if_quingo.set_verbose(True)
if_quingo.set_log_level(logging.DEBUG)

dir_path = Path(__file__).parent
kernel_file = dir_path / "grover.qu"
if (if_quingo.call_quingo(kernel_file, 'grover_2q') is not True):
    print("Fail to call the kernel")
res = if_quingo.read_result()
print(res)
