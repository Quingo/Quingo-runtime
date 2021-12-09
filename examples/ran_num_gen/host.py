import logging
from qgrtsys import if_quingo
import time

if_quingo.set_verbose(True)
if_quingo.set_log_level(logging.DEBUG)


def gen_ran_num(nr_rand_num):
    start = time.time()
    if if_quingo.call_quingo("kernel.qu",
                             'gen_ran_seq',
                             nr_rand_num):
        res = if_quingo.read_result()
        print("nr_rand_num: ", nr_rand_num)
        assert(len(res) == nr_rand_num)
        res = ''.join([str(int(r)) for r in res])
        print('the generated random sequence: ', res)
    end = time.time()
    return end - start


nr_rand_num = 1000
time1 = gen_ran_num(nr_rand_num)

print("The time cost to generate {} random numbers:".format(nr_rand_num))
print("{}: {:.2f}s".format(if_quingo.get_backend_name(), time1))
