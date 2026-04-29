"""The task of this module is to prepare the Quingo source file for the compilation."""

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


def extract_imports(qu_src: str) -> list[str]:
    """Extract import statements from a Quingo source file.

    Returns a list of module names (strings after 'import ').
    Comments are stripped before parsing.
    """
    src = remove_comment(qu_src)
    return re.findall(r"^\s*import\s+([\w.]+)", src, re.MULTILINE)


def gen_main_file(
    called_qg_fn: Path,
    called_qg_func: str,
    cl_entry_fn: Path,
    qg_params: tuple,
    qubit_alloc=None,
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
        qubit_alloc (Optional[List[str]]):
            an ordered list of physical qubit names to allocate inside main
            via a `using` block. When provided, each name becomes both:
              1. a `qubit`-typed allocation declared in `using (...)`;
              2. the leading positional argument(s) of the entry-function call,
                 in the same order. This lets the user write a fully
                 qubit-agnostic Quingo entry like
                 ``operation t1_experiment(q: qubit, t: time): unit { ... }``
                 and have the runtime bind it to a concrete physical qubit
                 (e.g. ``cq30``) at compile time, without modifying the .qu
                 source. When None or empty, behaviour is unchanged.
    """
    logger.setLevel(logging.WARNING)

    with called_qg_fn.open("r", encoding="utf-8") as qu_src_file:
        qu_src = qu_src_file.read()

    # Hoist imports from the user file so that embedded stdlib modules
    # (superconducting, std_ops, …) are imported at the entry-point level,
    # which is required for quingoc to load the corresponding .qfg semantics.
    transitive_imports = extract_imports(qu_src)
    all_imports = list(dict.fromkeys(transitive_imports + [called_qg_fn.stem]))
    import_block = "\n".join("import {}".format(m) for m in all_imports)

    main_func_str = gen_main_func(qu_src, called_qg_func, qg_params, qubit_alloc)
    try:
        content = import_block + "\n" + main_func_str
        cl_entry_fn.write_text(content)
    except:
        raise IOError("Cannot write the file: ", cl_entry_fn)


def gen_main_func(qu_src: str, called_op: str, qg_params: tuple, qubit_alloc=None):
    """This function is used to generate string version of the main
    function used to call quingo.

    Args:
        called_op (str) : the name of called Quingo operation._name`.
        qubit_alloc (Optional[List[str]]):
            see :func:`gen_main_file`.
    """

    var_name_list = []
    arg_str_list = []

    logger.debug(
        "calling function '{}' with parameters: {}, qubit_alloc: {}".format(
            called_op, qg_params, qubit_alloc
        )
    )

    if len(qg_params) != 0:
        for i, arg in enumerate(qg_params):
            var_name, var_def_str = dt.conv_arg_to_qg_str(i, arg)
            var_name_list.append(var_name)
            arg_str_list.append(var_def_str)

    ret_type = get_ret_type(qu_src, called_op)

    qubit_names = list(qubit_alloc) if qubit_alloc else []
    str_params = ", ".join(qubit_names + var_name_list)
    arg_strs = "\n".join(arg_str_list)
    if len(arg_strs) > 0:
        arg_strs = "\n" + arg_strs

    str_ret = "" if ret_type == "unit" else "return "

    func_call = "{ret}{func_name}({parameters});".format(
        ret=str_ret, func_name=called_op, parameters=str_params
    )

    if qubit_names:
        # Bind each requested physical qubit name to a `qubit` allocation in
        # the generated main, so that GateToPulse downstream sees a proper
        # AllocOp carrying `qubit_name = "cqXX"` after the inliner inlines
        # the user entry function. See proposal §0/§3 for the verification.
        using_decl = ", ".join("{}: qubit".format(n) for n in qubit_names)
        body = "{}\nusing ({}) {{\n{}\n}}".format(arg_strs, using_decl, func_call)
        func_str = "\noperation main() : {} {{{}\n}}".format(ret_type, body)
    else:
        func_str = "\noperation main() : {} {{{}\n{}\n}}".format(
            ret_type, arg_strs, func_call
        )

    return func_str
