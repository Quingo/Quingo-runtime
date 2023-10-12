import logging
from quingo import *
import sys
from os.path import abspath, dirname

sys.path.append(dirname(dirname(abspath(__file__))))
print(sys.path)
# import qututor.runtime.result_format as rf
# from qututor.tools import *
from my_utils import *

import termcolor as tc
import threading
from pathlib import Path

logger = get_logger("ctrl_adder")
logger.setLevel(logging.DEBUG)

mod_adder_module = Path(__file__).parent / "test_ctrl_adder.qu"
DEBUG_MODE = False


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


class Test_CtrlAdd:
    def ctrl_adder(params, debug):
        task = Quingo_task(mod_adder_module, "test_ctrl_adder", debug_mode=debug)

        c0, c1, a, b, w = params

        logger.debug(
            "ctrl_adder: c0: {}, c1: {}, a: {}, b: {}, w: {}".format(c0, c1, a, b, w)
        )

        exp_res = (a + b) if (c0 == 1 and c1 == 1) else b

        sim_result = call(task, params=(c0, c1, a, b, w))
        res = get_first_non_zero_res(sim_result)
        logger.info(
            "ctrl_adder "
            + (
                tc.colored("passed:", "green")
                if res == exp_res
                else tc.colored("failed:", "red")
            )
            + "c0: {}, c1: {}, a: {}, b: {}, w: {}, acutal: {}, expect: {}".format(
                c0, c1, a, b, w, res, exp_res
            )
        )
        assert res == exp_res

    def test_ctrl_adder(self):
        def single_test(params):
            if DEBUG_MODE:
                Test_CtrlAdd.ctrl_adder(params, DEBUG_MODE)
            else:
                t = threading.Thread(
                    target=Test_CtrlAdd.ctrl_adder, args=(params, DEBUG_MODE)
                )
                t.start()

        single_test((1, 1, 2, 3, 3))
        single_test((1, 1, 1, 5, 3))
        single_test((1, 1, 4, 5, 3))
        single_test((1, 0, 2, 3, 3))
        single_test((1, 0, 1, 5, 3))
        single_test((1, 0, 4, 5, 3))


if __name__ == "__main__":
    test = Test_CtrlAdd()
    test.test_ctrl_adder()
