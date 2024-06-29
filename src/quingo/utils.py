import sympy as sp
from pathlib import Path
import numpy as np
import os


def ensure_path(fn) -> Path:
    assert isinstance(fn, (str, Path))
    if isinstance(fn, str):
        fn = Path(fn).resolve()
    return fn


def validate_path(fn) -> Path:
    """
    Validates the given file path.

    Args:
        fn (str or Path): The file path to validate.

    Returns:
        Path: The validated file path as a `Path` object, or `None` if the path is invalid.
    """
    if not isinstance(fn, (str, Path)):
        return None

    if isinstance(fn, str):
        if os.path.isfile(fn):
            return Path(fn).resolve()
        else:
            return None

    if not fn.exists():
        return None
    else:
        return Path(fn).resolve()


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner


def number_distance(a, b):
    """calculates the distance between two complex numbers or two sympy numbers."""
    if isinstance(a, complex) and isinstance(b, complex):
        return (a.real - b.real) ** 2 + (a.imag - b.imag) ** 2

    if hasattr(a, "evalf") and hasattr(b, "evalf"):
        return (a.evalf() - b.evalf()) ** 2

    raise ValueError("unsupported types for dist: {} and {}".format(type(a), type(b)))


import numpy as np


def state_fidelity(state_a: np.ndarray, state_b: np.ndarray):
    """
    Calculate the state fidelity between two quantum states.

    Parameters:
    state_a (np.ndarray): The first quantum state.
    state_b (np.ndarray): The second quantum state.

    Returns:
    float: The state fidelity between the two quantum states.
    """
    return np.vdot(state_a, state_b)


def verify_qubit_map(qubit_map):
    num_qubits = len(qubit_map)
    inv_map = {v: k for k, v in qubit_map.items()}
    if set(inv_map.keys()) != set(qubit_map.keys()):
        raise ValueError("qubit map is not valid")

    for k, v in qubit_map.items():
        if inv_map[v] != k:
            raise ValueError("qubit map is not valid")


def shuffle_qubits_in_state(
    qubit_map: dict, old_qubit_order: list, state: np.ndarray
) -> np.ndarray:
    """This function shuffles the state vector, with the result representing the same state
    but the qubit order is changed according to the qubit_map.

    q0, q1, q2  ->  q2, q0, q1
    0   0   0   ->   0   0   0
    0   0   1   ->   1   0   0
    0   1   0   ->   0   0   1
    0   1   1   ->   1   0   1
    1   0   0   ->   0   1   0
    1   0   1   ->   1   1   0
    1   1   0   ->   0   1   1
    1   1   1   ->   1   1   1

    how to get the new idx for the old idx (idx_map)?
    1. get the qubit name for each index in the old qubit order (q1)
    2. get the new qubit index according to the qubit map (2)
    0 -> q0 -> 1
    1 -> q1 -> 2
    2 -> q2 -> 0
    idx_map = {0: 1, 1: 2, 2: 0}

    After having the new qubit index for each old qubit index, we can calculate the new index
    for the value in the new state vector. For example, we have a state vector with 3 qubits,
    and the qubit map is {0: 2, 1: 0, 2: 1}. We can calculate the new index for each value
    in the state vector by the following steps:
    1. get the binary representation of the old index.
    2. move the bit to the new position according to the idx_map.
    3. get the new index by converting the binary representation to an integer.

    so, new_state[new_idx] = state[old_idx], where new_idx = idx_map[old_idx]
    """
    verify_qubit_map(qubit_map)
    num_qubits = len(qubit_map)

    old_qubit_idx = {old_qubit_order[i]: i for i in range(num_qubits)}

    # qubit name list in the new order
    new_qubit_order = [qubit_map[k] for k in old_qubit_order]

    # dict: qubit name -> new qubit index
    new_qubit_idx = {new_qubit_order[i]: i for i in range(len(new_qubit_order))}

    # dict: old qubit index -> new qubit index
    idx_map = {}
    for i in range(num_qubits):
        qubit_name = old_qubit_order[i]
        this_old_qubit_idx = old_qubit_idx[qubit_name]
        this_new_qubit_idx = new_qubit_idx[qubit_name]
        idx_map[this_old_qubit_idx] = this_new_qubit_idx

    new_state = np.zeros_like(state)
    for i in range(len(state)):
        new_idx = 0
        for j in range(num_qubits):
            # select the j-th bit in i, and move it to the new position
            new_idx |= (((1 << j) & i) >> j) << idx_map[j]

        new_state[new_idx] = state[i]
    return new_state
