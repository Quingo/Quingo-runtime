import re
from .const import GATE_TRANSFORM


class BaseUtil():
    def __init__(self, qics):
        self.qcis = qics

    def find_qubit_by_qasm(self):
        qubit_idx = re.findall(r'Q(\d+)', self.qcis)
        return qubit_idx

    def package_qcis(self, qubit_idx, retrun_qasm):
        for idx, value in enumerate(qubit_idx):
            if int(value) < 0:
                raise Exception(
                    f'qcis:{self.qcis} qubit number cannot be less than 0')
            retrun_qasm += f'q[{int(value)}];\n' if int(
                idx) == len(qubit_idx) - 1 else f'q[{int(value)}],'
        return retrun_qasm

    def __str__(self):
        class_name = self.__class__.__name__
        qubit_idx = self.find_qubit_by_qasm()
        retrun_qasm = ''
        gate_tranform = GATE_TRANSFORM[class_name]
        if isinstance(gate_tranform, str) and gate_tranform:
            retrun_qasm += f'{gate_tranform} '
            retrun_qasm = self.package_qcis(qubit_idx, retrun_qasm)
        elif gate_tranform == '':
            retrun_qasm = ''
        elif isinstance(gate_tranform, list):
            gate = gate_tranform[0]
            qcis_parts = self.qcis.split()
            if len(gate_tranform) == 2:
                gate_param = gate_tranform[1]
                retrun_qasm += f'{gate}({gate_param}) '
            elif len(gate_tranform) == 1:
                if len(qcis_parts) > 2:
                    qcis_param = qcis_parts[2]
                    retrun_qasm += f'{gate}({qcis_param}) '
                else:
                    retrun_qasm += f'{gate} '
            elif len(gate_tranform) == 3:
                gate_param = gate_tranform[1:]
                if len(qcis_parts) > 3:
                    qcis_param1 = qcis_parts[3]
                    qcis_param2 = float(qcis_parts[2]) + gate_param[0]
                    qcis_param3 = gate_param[1] - float(qcis_parts[2])
                    retrun_qasm += f'{gate}({qcis_param1},{qcis_param2},{qcis_param3}) '
                else:
                    retrun_qasm += f'{gate} '
            retrun_qasm = self.package_qcis(qubit_idx, retrun_qasm)
        return retrun_qasm


def create_instruction_class(name, load_to_scope=False):
    cls = type(name, (BaseUtil,), {})
    if load_to_scope:
        scope = globals()
        if name not in scope:
            scope[name] = cls
    return cls


def load_qasm_classes():
    qcis_instructions = ['X', 'Y', 'Z', 'H', 'S', 'SD', 'T', 'TD', 'X2P',
                         'X2M', 'Y2P', 'Y2M', 'CZ', 'RZ', 'RX', 'RY', 'RXY', 'I', 'B', 'M']

    class_list = []
    for name in qcis_instructions:
        cls = create_instruction_class(name)
        class_list.append(cls)
    return class_list, qcis_instructions


(X, Y, Z, H, S, SD, T, TD, X2P,
 X2M, Y2P, Y2M, CZ, RZ, RX, RY,
 RXY, I, B, M), _QCIS_INSTRUCTIONS = load_qasm_classes()
