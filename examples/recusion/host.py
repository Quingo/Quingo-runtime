import logging
from quingo import *
from pathlib import Path

qu_file = Path(__file__).parent / "kernel.qu"


def routine(circ_name, num_shots=1):
    task = Quingo_task(qu_file, circ_name, debug_mode=logging.DEBUG)
    cfg = ExeConfig(ExeMode.SimStateVector, num_shots)
    res = call(
        task, (9,), BackendType.QUALESIM_QUANTUMSIM, cfg, config_fn="./std_qcis.qfg"
    )
    print("The result of {} is:".format(circ_name))
    print(res)


routine("apply_fib_n_h", 3)
