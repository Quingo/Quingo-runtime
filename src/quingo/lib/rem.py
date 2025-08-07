"""
Readout Error Mitigation
"""

# from qiskit import QuantumCircuit
import numpy as np
from scipy.optimize import minimize
from typing import Dict


def get_corr_exp_value_for_full_matrix_model(
    n_qubits: int,
    noisy_circ_prob: Dict[int, float],
    calibration_matrix,
) -> float:
    """
    Correct the unbiased estimator of expectation value

    Args:
        n_qubits: number of qubits
        noisy_circ_prob: probability distribution measured in pauli basis (eigenvector of observable) of target noisy circuit
        calibration_matrix: that is estimated value of full noise matrix

    Returns:
        corr_exp_value: corrected expectation value
    """

    if len(noisy_circ_prob) != 2**n_qubits:
        raise RuntimeError("incorrect length of arg noisy_circ_prob")
    noisy_prob_vector = np.zeros(2**n_qubits)
    for j in range(len(noisy_prob_vector)):
        noisy_prob_vector[j] = noisy_circ_prob.get(j, 0)
    # get prob corrected
    try:
        corr_prob_vector = np.linalg.inv(calibration_matrix) @ noisy_prob_vector
    except:
        corr_prob_vector = np.linalg.pinv(calibration_matrix) @ noisy_prob_vector
    negative_prob_occur = False
    for prob_value in corr_prob_vector:
        if prob_value < 0:
            negative_prob_occur = True
            break
    if not negative_prob_occur:
        corr_circ_prob = {i: corr_prob_vector[i] for i in range(len(corr_prob_vector))}
    else:  # may cost much time for a large number of qubit
        func = lambda x: np.linalg.norm(
            calibration_matrix @ x - noisy_prob_vector, ord=2
        )
        cons = [{"type": "eq", "fun": lambda x: sum(x) - 1}]
        for i in range(2**n_qubits):
            cons.append({"type": "ineq", "fun": lambda x, i=i: x[i]})
            cons.append({"type": "ineq", "fun": lambda x, i=i: 1 - x[i]})

        x0 = corr_prob_vector

        res = minimize(func, x0, method="SLSQP", constraints=cons)
        if res.success:
            corr_prob_vector = res.x
        corr_circ_prob = {i: corr_prob_vector[i] for i in range(len(corr_prob_vector))}

    return corr_circ_prob
    # corr_exp_value = 0
    # for state, prob in corr_circ_prob.items():
    #     if fmt_str.format(state).count("1") % 2 == 0:
    #         corr_exp_value += 1 * prob
    #     else:
    #         corr_exp_value += -1 * prob
    # return corr_exp_value


# Tensor Product Model


# def build_calibration_circuits_for_tensor_product_model(
#     n_qubits: int, observable: str
# ) -> Tuple[List[QuantumCircuit], List[str]]:
#     """ """

#     state_labels = ["0" * n_qubits, "1" * n_qubits]
#     calibration_circuits = []

#     for label in state_labels:
#         circ = QuantumCircuit(n_qubits)
#         for i in range(n_qubits):
#             if observable[::-1][i] == "Z":
#                 if label[::-1][i] == "1":
#                     circ.x(i)
#                 else:
#                     pass
#             elif observable[::-1][i] == "X":
#                 if label[::-1][i] == "1":
#                     circ.x(i)
#                     circ.h(i)
#                 else:
#                     circ.h(i)
#             elif observable[::-1][i] == "Y":
#                 if label[::-1][i] == "1":
#                     circ.x(i)
#                     circ.h(i)
#                     circ.s(i)
#                 else:
#                     circ.h(i)
#                     circ.s(i)
#             else:
#                 raise RuntimeError("unsupported observable")
#         calibration_circuits.append(circ)

#     return calibration_circuits, state_labels


# def cal_noise_matrix_for_tensor_product_model(
#     n_qubits: int, cali_circs_prob: List[Dict[int, float]]
# ):
#     """ """

#     calibration_matrices = []
#     fmt_str = "{:0" + str(n_qubits) + "b}"
#     for i in range(n_qubits):
#         noise_matrix_i = np.zeros((2, 2))
#         prob_0_1 = prob_1_0 = 0
#         for state, prob in cali_circs_prob[0].items():
#             if fmt_str.format(state)[::-1][i] == "1":
#                 prob_0_1 += prob
#         for state, prob in cali_circs_prob[1].items():
#             if fmt_str.format(state)[::-1][i] == "0":
#                 prob_1_0 += prob
#         noise_matrix_i[0][1] = prob_1_0
#         noise_matrix_i[1][1] = 1 - prob_1_0
#         noise_matrix_i[1][0] = prob_0_1
#         noise_matrix_i[0][0] = 1 - prob_0_1
#         calibration_matrices.append(noise_matrix_i)
#     return calibration_matrices


# def get_corr_exp_value_for_tensor_product_model(
#     n_qubits: int, noisy_circ_prob, calibration_matrices
# ):

#     fmt_str = "{:0" + str(n_qubits) + "b}"
#     corr_exp_value = 0
#     e_vector = np.array([1, 1])
#     pauli_Z = np.array([[1, 0], [0, -1]])
#     for state, prob in noisy_circ_prob.items():
#         tmp = 1
#         bin_str = fmt_str.format(state)
#         for i in range(n_qubits):
#             qubit_i_vector = np.zeros(2)
#             qubit_i_vector[int(bin_str[::-1][i])] = 1
#             tmp *= (
#                 e_vector
#                 @ pauli_Z
#                 @ np.linalg.inv(calibration_matrices[i])
#                 @ qubit_i_vector
#             )
#         corr_exp_value += tmp * prob

#     return corr_exp_value
