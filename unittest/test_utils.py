import pytest
import numpy as np
from quingo.utils import shuffle_qubits_in_state


@pytest.mark.parametrize(
    "qubit_map, old_qubit_order, state, expected_state",
    [
        (
            {"q0": "q1", "q1": "q0"},
            ["q0", "q1"],
            np.array([0, 1, 2, 3]),
            np.array([0, 2, 1, 3]),
        ),
        (
            {"q0": "q0", "q1": "q1"},
            ["q0", "q1"],
            np.array([0, 1, 2, 3]),
            np.array([0, 1, 2, 3]),
        ),
        (
            {"q0": "q2", "q1": "q0", "q2": "q1"},
            ["q0", "q1", "q2"],
            np.array([0, 1, 2, 3, 4, 5, 6, 7]),
            np.array([0, 4, 1, 5, 2, 6, 3, 7]),
        ),
        (
            {"q2": "q0", "q0": "q1", "q1": "q2"},
            ["q2", "q0", "q1"],
            np.array([0, 4, 1, 5, 2, 6, 3, 7]),
            np.array([0, 1, 2, 3, 4, 5, 6, 7]),
        ),
    ],
)
def test_shuffle_qubits_in_state(qubit_map, old_qubit_order, state, expected_state):
    shuffled_state = shuffle_qubits_in_state(qubit_map, old_qubit_order, state)
    np.testing.assert_array_equal(shuffled_state, expected_state)
