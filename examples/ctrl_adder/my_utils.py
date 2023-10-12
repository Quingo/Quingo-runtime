def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


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



import logging
from logging.handlers import TimedRotatingFileHandler
import sys
import colorama as cm
import termcolor as tc
from pathlib import Path

cm.init()

# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Style: DIM, NORMAL, BRIGHT, RESET_ALL


def quingo_info(arg, **kwargs):
    print(arg, **kwargs)


def quingo_msg(arg, **kwargs):
    print(tc.colored(arg, "green"), **kwargs)


def quingo_warning(arg, **kwargs):
    print(tc.colored(arg, "yellow"), **kwargs)


def quingo_err(arg, **kwargs):
    print(tc.colored(arg, "red"), **kwargs)


FORMATTER = logging.Formatter(
    "%(asctime)s %(name)s %(lineno)d(%(levelname)s): %(message)s", datefmt="%H:%M:%S"
)
# LOG_FILE = "my_app.log"


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


# def get_file_handler():
#     file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
#     file_handler.setFormatter(FORMATTER)
#     return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    # better to have too much log than not enough
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler())
    # logger.addHandler(get_file_handler())
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger


def ensure_path(fn) -> Path:
    assert isinstance(fn, (str, Path))
    if isinstance(fn, str):
        fn = Path(fn).resolve()
    return fn



if __name__ == "__main__":
    test_int2bits()
