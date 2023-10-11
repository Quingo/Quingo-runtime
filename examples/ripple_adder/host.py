import logging
from quingo import *
from pathlib import Path

qu_file = Path(__file__).parent / "kernel.qu"


def routine(circ_name, num_qubits=1, a=[0], b=[0]):
    task = Quingo_task(qu_file, circ_name)
    cfg = ExeConfig(ExeMode.SimFinalResult)
    res = call(task,(num_qubits,a,b,),BackendType.DQCSIM_QUANTUMSIM,cfg)
    return res


def get_value(d):
    res = [""]*len(d[1])
    for i in range(len(d[1])):
        for j in reversed(d[1][i]):
            res[i] = res[i]+str(j)
    return res


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
    print(res)
    
    bin_output = get_value(res)
    print("result binary from the quantum kernel:", bin_output)
    output = int(bin_output[0], 2)
    print("The result of Ripple Adder is: {}".format(output))
    return output


a = 3
b = 5
assert (adder_output(a, b) == a + b)
