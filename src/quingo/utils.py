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
