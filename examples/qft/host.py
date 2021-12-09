from qgrtsys import If_Quingo
import time

if_quingo = If_Quingo(backend='pyqcisim_quantumsim')

if_quingo.call_quingo("qft.qu", 'qft4')
res = if_quingo.read_result()
print(res)
