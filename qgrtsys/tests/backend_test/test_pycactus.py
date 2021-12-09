from qgrtsys import If_Quingo
from pathlib import Path

if_quingo = If_Quingo(backend='PyCACTUS_QuantumSim')
kernel_file = Path(__file__).parent / "kernel.qu"

if if_quingo.call_quingo(kernel_file, 'gen_ran'):
    res = if_quingo.read_result()
    print("res: ", res)
else:
    print("failed to call the quantum kernel qrng@kernel.qu.")
