import logging
from quingo import *
import sys
from os.path import abspath, dirname
import termcolor as tc
import threading
from pathlib import Path
from my_utils import *

sys.path.append(dirname(dirname(abspath(__file__))))


def get_first_non_zero_res(sim_result, integer_format=True):
    """This function is used to get the first non-zero result from the measurement results.

    sim_result format: (qubit_list, msmt res list).
        An Example result of a simulation with num_shots=3:
            ```
            (['Q3', 'Q4', 'Q5', 'Q6', 'Q7'],
            [[1, 1, 0, 0, 0],
                [1, 1, 0, 0, 0],
                [1, 1, 0, 0, 0]])
            ```
    return: the first non-zero result (in integer format) in the measurement results.
    """
    if sim_result is None:
        raise ValueError("No measure results found")
    _, msmt_res = sim_result

    if msmt_res is None:
        raise ValueError("No measure results found")

    res = msmt_res[0]
    res.reverse()
    if integer_format:
        return int("".join(map(str, res)), 2)
    else:
        return msmt_res[0]


logger = get_logger("adder_test")
logger.setLevel(logging.INFO)

dir_path = Path(__file__).parent.resolve()
kernel_file = Path(__file__).parent / "draper_test.qu"
print("kernel_file: ", kernel_file.resolve())


def trigger_task(func, args, multi_threading):
    if multi_threading:
        t = threading.Thread(target=func, args=args)
        t.start()
    else:
        func(*args)


class Test_Draper_adder:
    def add_or_sub(i, j, num_qubits, subtract=False):
        task = Quingo_task(kernel_file, "test_sc_adder")
        i_bits = int2bit_list(i, num_qubits)
        j_bits = int2bit_list(j, num_qubits)
        logger.debug("a: {} '{}'   b: {} '{}'".format(i, bin(i), j, bin(j)))

        sim_result = call(task, (i_bits, j_bits, subtract))
        logger.debug(sim_result)
        res = get_first_non_zero_res(sim_result)
        logger.debug("res: {}".format(res))
        logger.debug(" {}  {}  {}".format(i, j, res))

        if subtract:
            assert res == subtracter_behavior(i, j, num_qubits)
        else:
            assert res == adder_behavior(i, j, num_qubits)

        logger.info(
            tc.colored("passed:", "green")
            + " {} {} {} = {}".format(i, "-" if subtract else "+", j, res)
        )

    def test_adder(self, subtract=False):
        num_qubits = 3
        for i in range(1 << 2):
            for j in range(1 << 2):
                trigger_task(Test_Draper_adder.add_or_sub, (i, j, num_qubits), True)

    def test_subtracter(self):
        num_qubits = 3
        for i in range(1 << 2):
            for j in range(1 << 2):
                trigger_task(
                    Test_Draper_adder.add_or_sub, (i, j, num_qubits, True), True
                )


if __name__ == "__main__":
    Test_Draper_adder().test_adder()
    Test_Draper_adder().test_subtracter()
