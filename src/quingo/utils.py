import sympy as sp


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
