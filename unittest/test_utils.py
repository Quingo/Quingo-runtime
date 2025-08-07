import pytest
import numpy as np
from quingo.utils import shuffle_qubits_in_state


@pytest.mark.parametrize(
    "old_qubit_order, new_qubit_order, state, expected_state",
    [
        (
            ["q0", "q1"],
            ["q1", "q0"],
            np.array([0, 1, 2, 3]),
            np.array([0, 2, 1, 3]),
        ),
        (
            ["q0", "q1"],
            ["q0", "q1"],
            np.array([0, 1, 2, 3]),
            np.array([0, 1, 2, 3]),
        ),
        (
            ["q0", "q1", "q2"],
            ["q2", "q0", "q1"],
            np.array([0, 1, 2, 3, 4, 5, 6, 7]),
            np.array([0, 4, 1, 5, 2, 6, 3, 7]),
        ),
        (
            ["q2", "q0", "q1"],
            ["q0", "q1", "q2"],
            np.array([0, 4, 1, 5, 2, 6, 3, 7]),
            np.array([0, 1, 2, 3, 4, 5, 6, 7]),
        ),
    ],
)
def test_shuffle_qubits_in_state(
    old_qubit_order, new_qubit_order, state, expected_state
):
    shuffled_state = shuffle_qubits_in_state(old_qubit_order, new_qubit_order, state)
    np.testing.assert_array_equal(shuffled_state, expected_state)


@pytest.mark.parametrize(
    "old_qubit_order, new_qubit_order",
    [
        ([0, 1, 2, 3], [2, 3, 1, 0]),
        ([0, 1, 2, 3], [3, 2, 1, 0]),
        ([0, 1, 2, 3, 4], [2, 4, 3, 1, 0]),
        ([2, 4, 3, 1, 0], [0, 1, 2, 3, 4]),
        ([0, 1, 2, 3, 4, 5], [2, 4, 3, 5, 1, 0]),
        ([0, 1, 2, 3, 4, 5, 6], [2, 6, 4, 3, 5, 1, 0]),
        ([0, 1, 2, 3, 4, 5, 6, 7], [2, 7, 1, 3, 5, 4, 6, 0]),
    ],
)
def test_single_value_state(old_qubit_order, new_qubit_order):

    num_qubits = len(old_qubit_order)

    old_name_2_idx_map = {old_qubit_order[i]: i for i in range(num_qubits)}
    new_name_2_idx_map = {new_qubit_order[i]: i for i in range(num_qubits)}

    for idx in range(num_qubits):
        qubit_name = old_qubit_order[idx]

        state = np.zeros(2**num_qubits)
        state[1 << old_name_2_idx_map[qubit_name]] = 1  # pure state, e.g., |0010>
        print("state: ", state)

        exp_state = np.zeros(2**num_qubits)
        # pure state after shuffling, e.g., |0100>
        exp_state[1 << new_name_2_idx_map[qubit_name]] = 1
        print("exp_state: ", exp_state)

        shuffled_state = shuffle_qubits_in_state(
            old_qubit_order, new_qubit_order, state
        )
        print("shuffled_state: ", shuffled_state)
