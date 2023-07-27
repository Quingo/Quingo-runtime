import logging
from quingo import quingo_interface as qi
from pathlib import Path


qi.connect_backend('pyqcisim_quantumsim')

qu_file = Path(__file__).parent / "kernel.qu"


def routine(circ_name, num_qubits=1, a=[0], b=[0]):
    qi.call_quingo(qu_file, circ_name, num_qubits, a, b)
    res = qi.read_result()
    return res


def get_keys(d):
    return [k for k, v in d.items() if v > 0]


def transform_input(Input_1, Input_2):
    bin_a = "{0:b}".format(Input_1)
    bin_b = "{0:b}".format(Input_2)
    num_bits = max(len(bin_a), len(bin_b))

    def get_bit_list(bin_str, target_len):
        full_len_bin_str = '{:0>{width}}'.format(bin_str, fill='0', width=target_len)
        return [int(bit) for bit in full_len_bin_str]

    bit_list_a = get_bit_list(bin_a, num_bits)
    bit_list_b = get_bit_list(bin_b, num_bits)
    return (num_bits, bit_list_a, bit_list_b)


def adder_output(In_a, In_b):
    print("the input integers are {} and {}.".format(In_a, In_b))
    num_bits, bit_list_a, bit_list_b = transform_input(In_a, In_b)
    print("binary representation of a and b: {} and {}".format(bit_list_a, bit_list_b))
    res = routine("ripple_adder", num_bits, bit_list_a, bit_list_b)
    bin_output = get_keys(res[1])
    print("result binary from the quantum kernel:", bin_output)
    output = int(bin_output[0], 2)
    print("The result of Ripple Adder is: {}".format(output))
    return output


a = 3
b = 5
assert (adder_output(a, b) == a + b)
