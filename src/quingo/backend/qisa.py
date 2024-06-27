import enum


class Qisa(enum.Enum):
    QCIS = enum.auto()
    QUIET = enum.auto()
    BRANCH_QUIET = enum.auto()
    eQASM = enum.auto()
    Quantify = enum.auto()


def get_qisa_name(qisa: Qisa):
    """Get the name of the qisa type which is used by the compiler"""
    assert isinstance(qisa, Qisa)

    if qisa == Qisa.QCIS:
        return "qcis"
    if qisa == Qisa.QUIET:
        return "quiets"
    if qisa == Qisa.BRANCH_QUIET:
        return "branch-quiets"
    if qisa == Qisa.eQASM:
        return "eqasm"
    if qisa == Qisa.Quantify:
        return "quantify"

    raise ValueError("unknown qisa type: {}".format(qisa))


def get_suffix(qisa: Qisa):
    """Get the suffix of the corresponding qisa file"""
    assert isinstance(qisa, Qisa)

    if qisa == Qisa.QCIS:
        return ".qcis"
    if qisa == Qisa.QUIET or qisa == Qisa.BRANCH_QUIET:
        return ".qi"
    if qisa == Qisa.eQASM:
        return ".eqasm"
    if qisa == Qisa.Quantify:
        return ".json"

    raise ValueError("unknown qisa type: {}".format(qisa))
