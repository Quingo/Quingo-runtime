from quingo import Quingo_interface
from pathlib import Path

quingo_interface = Quingo_interface(backend="PyQCISim_quantumsim")
kernel_file = Path(__file__).parent / "kernel.qu"

if quingo_interface.call_quingo(kernel_file, "qrng"):
    print(quingo_interface.get_last_qasm())
    res = quingo_interface.read_result()
    print("res: ", res)
else:
    print("failed to call the quantum kernel qrng@kernel.qu.")
