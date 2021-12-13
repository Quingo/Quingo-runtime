from quingo import Quingo_interface
from pathlib import Path

quingo_interface = Quingo_interface(backend='PyQCAS_QuantumSim')
kernel_file = Path(__file__).parent / "kernel.qu"

if quingo_interface.call_quingo(kernel_file, 'gen_ran'):
    res = quingo_interface.read_result()
    print("res: ", res)
else:
    print("failed to call the quantum kernel qrng@kernel.qu.")
