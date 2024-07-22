from quingo import *
import numpy as np
from pathlib import Path
from typing import List, Dict


def cal_noise_matrix_for_full_matrix_model(
    n_qubits: int, cali_circs_prob: List[Dict[int, float]]
):
    """
    Calculate the noise matrix through measuring the probability distribution of calibration circuits

    Args:
        n_qubits: number of qubits
        cali_circs_probs: probability distributions measured in pauli basis (eigenvector of observable) of calibration circuits

    Returns:
        calibration_matrix: that is estimated value of full noise matrix
    """
    calibration_matrix = np.zeros((2**n_qubits, 2**n_qubits))
    for i in range(len(cali_circs_prob)):
        for label, value in cali_circs_prob[i].items():
            calibration_matrix[label][i] = value

    return calibration_matrix


def get_prob_noisy(task: Quingo_task, noise_config, n_qubits, params=(), shots=32000):
    cfg = ExeConfig(ExeMode.SimProbability, num_shots=shots, noise_config=noise_config)
    qasm_fn = compile(task, params=params)
    sim_result = execute(qasm_fn, BackendType.TEQUILA, cfg)
    dic = {}
    for i in range(len(sim_result[1])):
        dic[i] = sim_result[1][i].real
    return dic


def b_get_prob_noisy(task: Quingo_task, noise_config, n_qubits, params=(), shots=32000):
    cfg = ExeConfig(ExeMode.SimShots, num_shots=shots, noise_config=noise_config)
    qasm_fn = compile(task, params=params)
    sim_result = execute(qasm_fn, BackendType.TEQUILA, cfg)

    def count_elements(lst):
        return np.unique(np.array(lst), return_counts=True, axis=0)

    res = count_elements(sim_result[1])

    def list_to_int(bit_list):
        return sum(1 << i for i, bit in enumerate(bit_list) if bit)

    dic = {}
    for i in range(2**n_qubits):
        dic[i] = 0
    for i in range(len(res[0])):
        dic[list_to_int(res[0][i])] = res[1][i] / shots
    return dic


def int_to_list(number, bit_length=None):
    if bit_length is None:
        bit_length = number.bit_length() if number >= 0 else 1
    binary_list = [(number >> i) & 1 for i in range(bit_length - 1, -1, -1)]
    return binary_list


qu_calibration = Path("calibration_circuits.qu")
calibration_circ = Quingo_task(qu_calibration, "calibration_circuits")


def calibration_matrix(calibration_circ, nqubits, observable, noise_config):
    cali_circs_fm = []
    for ii in range(2**nqubits):
        paramsi = (nqubits, observable, int_to_list(ii, nqubits))
        cali_circs_fm.append(paramsi)
    cali_circs_prob_fm = [
        b_get_prob_noisy(calibration_circ, noise_config, nqubits, params, shots=100)
        for params in cali_circs_fm
    ]
    cali_matrix_fm = cal_noise_matrix_for_full_matrix_model(nqubits, cali_circs_prob_fm)
    return cali_matrix_fm
