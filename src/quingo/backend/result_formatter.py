def reorder_bits(qubit_list, str_bit_list, Ascending=True):
    """Reorder the bits in str_bit_list according to the order of qubit_list.
    Given qubit list ["Q2", "Q1", "Q4", "Q3"] and `str_bit_list` "0001",
    the ordered result is "0010", which corresponds to ["Q1", "Q2", "Q3", "Q4"].
    """

    num_qubits = len(qubit_list)

    qubit_result_pair = [(qubit_list[i], str_bit_list[i]) for i in range(num_qubits)]

    qubit_result_pair.sort(key=lambda x: int(x[0][1:]), reverse=not Ascending)

    print(qubit_result_pair)

    return "".join([x[1] for x in qubit_result_pair])


def get_first_non_zero_res(qcis_result):
    """This function is used to get the first non-zero result from the measurement results.

    qcis_result format: (qubit_list, msmt_count), where qubit_list is a list of qubit names, and msmt_count is a dictionary of measurement results.

    return: the first non-zero result (in integer format) in the measurement results.
    """
    if qcis_result is None:
        print("No measure results found")
    qubit_list, msmt_count = qcis_result
    for k, v in msmt_count.items():
        if v > 0:
            ordered_str = reorder_bits(qubit_list, k)
            return int(ordered_str, 2)
