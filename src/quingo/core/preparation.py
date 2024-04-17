"""The task of this module is to prepare the Quingo source file for the compilation.
"""

import re
from pathlib import Path
import logging
from quingo.core.quingo_logger import get_logger
import quingo.core.data_transfer as dt

logger = get_logger((__name__).split(".")[-1])


def remove_comment(qu_src):
    search_annotation_string = r"\/\/.*\n"
    return re.sub(search_annotation_string, "", qu_src)


def get_ret_type(qu_src: str, qg_func_name: str):
    """This function read the Quingo source file to retrieve the return
    type (in str format) of called Quingo operation.

    Args:
        qu_src (str) :  the Quingo source containing the called operation.
        qg_func_name (str) : the name of the Quingo function.
    """
    qu_src = remove_comment(qu_src)

    search_string = r"\boperation\b\s+" + qg_func_name + r"\s*\((.*)\)\s*:(.*)\s*\{"

    op_def_components = re.search(search_string, qu_src)
    if op_def_components is None:
        raise ValueError(
            "Cannot find the operation ({}) in the given Quingo source "
            "file: \n```\n{}\n```".format(qg_func_name, qu_src)
        )

    ret_type = re.sub(r"\d", "", op_def_components.groups()[1].strip())
    if ret_type == "":
        ret_type = "unit"
    return ret_type


def gen_main_file(
    called_qg_fn: Path, called_qg_func: str, cl_entry_fn: Path, qg_params: tuple
):
    """This function generates the main function required to perform
    compilation. A new file named 'main_<qg_filename>' under the
    `<build_dirname>` directory is generated to allocate this main
    function.

    Args:
        called_qg_fn (Path) :
            the path of the Quingo file which contains the quantum
            function called by the host program.
        called_qg_func (str) :
            the name of the Quingo function.
        cl_entry_fn (Path) :
            compilation entry file, which contains the generated  main function
        args (list):
            a variable length of parameters passed to the quantum function
    """
    logger.setLevel(logging.WARNING)
    import_stmt = "import {}".format(called_qg_fn.stem)

    with called_qg_fn.open("r", encoding="utf-8") as qu_src_file:
        qu_src = qu_src_file.read()

    main_func_str = gen_main_func(qu_src, called_qg_func, qg_params)
    try:
        content = import_stmt + "\n" + main_func_str
        cl_entry_fn.write_text(content)
    except:
        raise IOError("Cannot write the file: ", cl_entry_fn)


def gen_main_func(qu_src: str, called_op: str, qg_params: tuple):
    """This function is used to generate string version of the main
    function used to call quingo.

    Args:
        called_op (str) : the name of called Quingo operation._name`.
    """

    var_name_list = []
    arg_str_list = []

    logger.debug(
        "calling function '{}' with parameters: {}".format(called_op, qg_params)
    )

    if len(qg_params) != 0:
        for i, arg in enumerate(qg_params):
            var_name, var_def_str = dt.conv_arg_to_qg_str(i, arg)
            # print("var_name: ", var_name)
            # print("var_def_str: ", var_def_str)
            var_name_list.append(var_name)
            arg_str_list.append(var_def_str)

    # qu_src = None
    # with called_qg_fn.open("r", encoding="utf-8") as qu_src_file:
    #     qu_src = qu_src_file.read()
    ret_type = get_ret_type(qu_src, called_op)

    str_params = ", ".join(var_name_list)
    arg_strs = "\n".join(arg_str_list)
    if len(arg_strs) > 0:
        arg_strs = "\n" + arg_strs

    str_ret = "" if ret_type == "unit" else "return "

    func_call = "{ret}{func_name}({parameters});".format(
        ret=str_ret, func_name=called_op, parameters=str_params
    )

    func_str = "\noperation main() : {} {{{}\n{}\n}}".format(
        ret_type, arg_strs, func_call
    )

    return func_str
