def adder_behavior(a, b, num_qubits):
    return (a + b) % (1 << num_qubits)


def subtracter_behavior(a, b, num_qubits):
    if a >= b:
        return a - b
    else:
        return (1 << num_qubits) - (b - a)


def get_bin(x, n):
    if not is_number(x):
        raise ValueError("get_bin: parameter is not a number.")

    return "{0:{fill}{width}b}".format((int(x) + 2**n) % 2**n, fill="0", width=n)


def int2bit_list(x, n):
    """Convert an interger `x` to a `n`-bit bit list."""
    if not (0 <= x < 2**n):
        raise ValueError(
            "int2bit_list: x ({}) is not in the range [0, {}).".format(x, 2**n)
        )
    bits = [x >> i & 1 for i in range(n)]
    return bits


def test_int2bits():
    assert int2bit_list(0, 3) == [0, 0, 0]
    assert int2bit_list(1, 3) == [1, 0, 0]
    assert int2bit_list(3, 3) == [1, 1, 0]
    assert int2bit_list(7, 3) == [1, 1, 1]
    assert int2bit_list(1089, 15) == [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]


if __name__ == "__main__":
    test_int2bits()
