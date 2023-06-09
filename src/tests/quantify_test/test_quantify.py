from quingo import Quingo_interface
from pathlib import Path

quingo_interface = Quingo_interface(backend="quantify")
kernel_file = Path(__file__).parent / "kernel.qu"

if quingo_interface.call_quingo_compiler(kernel_file, "t1", 40):
    res = quingo_interface.get_last_qasm()
    print("res: ", res)
else:
    print("failed to call the quantum kernel qrng@kernel.qu.")
