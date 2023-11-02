import logging
from quingo import *
from pathlib import Path
import matplotlib.pyplot as plt

# from scipy.optimize import minimize_scalar, minimize
from numpy import *
import numpy as np

cfg = ExeConfig(ExeMode.SimStateVector, 10)

qu_file = Path(__file__).parent / "kernel.qu"


def get_ansatz(circ_name, theta):
    task = Quingo_task(qu_file, circ_name)
    # res = call(task, (theta,), BackendType.QUALESIM_TEQUILA, cfg,config_fn="./std_qcis.qfg")
    qasm_fn = compile(task, params=(theta,), config_file="./std_qcis.qfg")
    res = execute(qasm_fn, BackendType.QUANTUM_SIM, cfg)
    print(res)
    return res


# eval_all()
get_ansatz("ansatz", 0.0)
