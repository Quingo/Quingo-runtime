# 1. 构造哈密顿量
from Hamiltonian import hamiltonian
from ansatz import get_ansatz

# 验证 hamiltonian 的正确性
"""
from qiskit_nature.units import DistanceUnit
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper
import qiskit_nature.settings

qiskit_nature.settings.use_pauli_sum_op = False

driver = PySCFDriver(
    atom="H 0 0 0; H 0 0 0.735",
    basis="sto3g",
    charge=0,
    spin=0,
    unit=DistanceUnit.ANGSTROM,
)
problem = driver.run()
mapper = JordanWignerMapper()
H2_op = mapper.map(problem.hamiltonian.second_q_op())

H1 = H2_op.to_matrix()
# print(H1)
H2 = hamiltonian(H2_op.paulis, H2_op.coeffs)
assert (H1 == H2).all()
"""
"./std_qcis.qfg"
# 2. 生成 ansatz 电路
"""
from pathlib import Path
from quingo import *
qu_file = Path(__file__).parent / "kernel.qu"
# input circuit name.
circ_name = "ansatz"
cfg = ExeConfig(ExeMode.SimStateVector)
params = (0.1,)
get_ansatz(qu_file, circ_name, params, config_file="./std_qcis.qfg")
"""

# 3. 优化
# from scipy.optimize import minimize_scalar, minimize
from scipy.optimize import minimize_scalar, minimize
import matplotlib.pyplot as plt
import numpy as np
from quingo import *
from pathlib import Path
from typing import List
import random


def get_real(c):
    return np.real(c)


def expectation(h, state):
    """Return the expectation value of the given state under the given hamiltonian."""
    state_matrix = np.mat(state).T
    t_conj_state = state_matrix.T.conjugate()
    return get_real(np.dot(t_conj_state, np.dot(h, state_matrix)))


def energy_theta(qu_file, circ_name, backend, params: np.array, paulis, coeffs):
    """Return the calculated energy for the given parameter theta."""
    pr = tuple(params)
    ansatz_state = get_ansatz(
        qu_file, circ_name, backend, params=pr, config_file="./std_qcis.qfg"
    )
    h = hamiltonian(paulis, coeffs)
    energy = expectation(h, ansatz_state)
    print(energy)
    return energy


def vqe(
    qu_file,
    circ_name,
    num_theta: int,
    paulis,
    coeffs,
    backend=BackendType.QUANTUM_SIM,
    method="Nelder-Mead",
):
    """Return the calculated energy for the given parameter theta."""

    def func(params):
        return energy_theta(qu_file, circ_name, backend, params, paulis, coeffs).A[0][0]

    theta = random.uniform(0, 2 * np.pi)
    x1 = np.array([theta] * num_theta)
    minimum = minimize(fun=func, x0=x1, method=method)
    return minimum
