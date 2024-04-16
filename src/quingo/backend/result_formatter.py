from typing import List, Tuple


def reorder_bits(qubit_list, qubit_msmt_res, Ascending=True):
    """
    Given the measurement result `qubit_msmt_res` of `qubit_list`, reorder the bits in the
    result according to the qubit name order.

    Args:
        qubit_list (list): A list of qubit names in the desired order.
        qubit_msmt_res (list): A list of measurement results corresponding to the qubits.
        Ascending (bool, optional): Specifies whether the bits should be reordered in ascending order.
            Defaults to True.

    Returns:
        list: A list of reordered measurement results.

    Example:
        Given qubit list ["Q3", "Q1", "Q4", "Q2"] and `qubit_msmt_res` [1, 1, 0, 0],
        the ordered result is [1, 0, 1, 0], which corresponds to ["Q1", "Q2", "Q3", "Q4"].
    """
    num_qubits = len(qubit_list)

    qubit_result_pair = [
        (qubit_list[i].lower(), qubit_msmt_res[i]) for i in range(num_qubits)
    ]

    qubit_result_pair.sort(key=lambda x: int(x[0][1:]), reverse=not Ascending)

    print(qubit_result_pair)

    return [x[1] for x in qubit_result_pair]


def get_first_non_zero_res(
    shots_result: Tuple[List[str], List[List[int]]],
    qubits: List[str] = None,
    integer_format=True,
    little_endian=True,
):
    """
    This function is used to get the first non-zero result from the measurement results.

    Args:
        shots_result (tuple): A tuple containing two elements: a list of qubit names and a list
          of measurement results.
            An example shots result of a simulation with num_shots = 3:
            (['Q3', 'Q4', 'Q5', 'Q6', 'Q7'],
               [[1, 1, 0, 0, 0],
                [1, 1, 0, 0, 0],
                [1, 1, 0, 0, 0]])

        qubits (list, optional): A list of qubit names. If provided, the function will only consider
          the measurement results of the specified qubits.
            Defaults to None.

        integer_format (bool, optional): Specifies whether the result should be returned as an
          integer or as a list of bits.
            Defaults to True.

        little_endian (bool, optional): Specifies whether the result should be in little-endian
        format. If False, the result is in big-endian format.
            Defaults to True.
            Little-endian: [Q0, Q1, Q2] [1, 0, 0] -> 1
            Big-endian:    [Q0, Q1, Q2] [1, 0, 0] -> 4

    Returns:
        int or list: The first non-zero result in the measurement results. If `integer_format` is
          True, the result is returned as an integer.
        Otherwise, the result is returned as a list of bits.

    Raises:
        ValueError: If `shots_result` is None or if the measurement results are None.
    """
    if shots_result is None:
        raise ValueError("No measure results found")
    names, msmt_res = shots_result

    if msmt_res is None:
        raise ValueError("No measure results found")

    res = msmt_res[0]
    if qubits is not None:
        indices = [names.index(q) for q in qubits]
        res = [res[idx] for idx in indices]

    if little_endian:
        res.reverse()

    if integer_format:
        return int("".join(map(str, res)), 2)
    else:
        return msmt_res[0]
