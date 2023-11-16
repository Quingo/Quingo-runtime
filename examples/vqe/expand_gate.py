from typing import List
from math import log2

# from utils import remap_bits, gamma
import numpy as np


def get_bit(val, n):
    """Get the n-th bit of val.

    No check is performed.
    """
    return val >> n & 1


def remap_bits(val, bit_pos_list):
    """Remap the bits of val according to bit_pos_list, i.e.,
    $$
    \sum_{i=0}^{l - 1}{val\langle i\rangle \times 2^{bit_pos_list[i]}}
    $$
    where, $val\langle i\rangle$ is the i-th bit of val.
    """
    sum = 0
    for i in range(len(bit_pos_list)):
        sum += get_bit(val, i) << bit_pos_list[i]
    return sum


def gamma(t_val, t_qubits, o_val, o_qubits, c_val=0, c_qubits=[]):
    """This function calculates the following value:
        $$
        \Gamma(k,x)|_{\{o_0, o_1, \cdots, o_{l-1}\}, \{t_0, t_1, \cdots, t_{n-1}\}} = \sum_{i=0}^{l -1}{k\langle i\rangle \times 2^{o_i}} + \sum_{i=0}^{n-1}{x\langle i\rangle \times 2^{t_i}}
        $$
    i.e., $\overline{o_{l-1}\cdots b_{n-1}o_{l-2}\cdots b_{n-2}\cdots b_{0}o_{0}}$.
    This value is used in expanding a matrix when applying a gate on qubits.

    Parameters
    ----------
    t_qubits : list of integers
        a list of target qubits
    o_qubits : list of integers
        a list of other qubits
    t_val : an integer value
        it should have the same length as t_qubits
    o_val : an integer value
        it should have the same length as o_qubits

    Returns
    -------
    integer
        the value of $\Gamma(k,x)$
    """
    if c_qubits == []:
        return remap_bits(o_val, o_qubits) + remap_bits(t_val, t_qubits)
    else:
        return (
            remap_bits(o_val, o_qubits)
            + remap_bits(t_val, t_qubits)
            + remap_bits(c_val, c_qubits)
        )


def expand_gate(num_qubits, core_mat: np.matrix, t_qubits: List[int]):
    """
    Expand a gate to a matrix of the entire circuit.
    The size of the matrix is determined by the total number of qubits in the circuit.

    Args:
        num_qubits: The number of qubits in the circuit.
        core_mat: The matrix of the gate to be expanded.
        t_qubits: The target qubits of the gate.
    """
    if log2(core_mat.shape[0]) != len(t_qubits):
        raise ValueError("The number of qubits is not correct")

    o_qubits = []
    used_qubits = t_qubits
    for i in range(num_qubits):
        if i not in used_qubits:
            o_qubits.append(i)

    num_target_qubits = len(t_qubits)
    num_other_qubits = len(o_qubits)

    assert num_qubits == num_target_qubits + num_other_qubits

    new_mat_size = 2**num_qubits
    new_mat = np.zeros((new_mat_size, new_mat_size), dtype=complex)

    for o_val in range(2**num_other_qubits):
        for tgt_idx in range(2**num_target_qubits):
            iden_idx = remap_bits(o_val, o_qubits) + remap_bits(tgt_idx, t_qubits)
            new_mat[iden_idx, iden_idx] = 1

        for t_val in range(2**num_target_qubits):
            for i in range(2**num_target_qubits):
                row_idx = gamma(t_val, t_qubits, o_val, o_qubits)
                col_idx = gamma(i, t_qubits, o_val, o_qubits)
                new_mat[row_idx, col_idx] = core_mat[t_val, i]
    return np.matrix(new_mat)
