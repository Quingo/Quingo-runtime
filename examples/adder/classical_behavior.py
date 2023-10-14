def adder_behavior(a, b, num_qubits):
    return (a + b) % (1 << num_qubits)


def subtracter_behavior(a, b, num_qubits):
    if a >= b:
        return a - b
    else:
        return (1 << num_qubits) - (b - a)
