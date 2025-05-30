from .qcis import *
from .const import GATE_TRANSFORM


class QcisToQasm():
    def __init__(self):
        pass

    def get_gate_by_name(self, gate_name):
        gate = globals()[gate_name]
        return gate

    def find_qubit_idx_by_qasm(self, qcis):
        qubit_idx = re.findall(r'Q(\d+)', qcis)
        return qubit_idx

    def convert_qcis_to_qasm(
            self,
            qcis: str):
        """
            convert qasm to qcis

            Args:
                qcis: qcis

            Returns:
                str: return the converted qasm.
        """
        qcis = qcis.upper()
        qcis_instruction_list = qcis.split('\n')
        qcis_instruction_list = [
            inst.strip() for inst in qcis_instruction_list if qcis.strip()]
        qubit_idx = self.find_qubit_idx_by_qasm(qcis)
        qreg_qubit = max([int(idx) for idx in qubit_idx])
        qasm = f'''OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[{qreg_qubit+1}];\ncreg c[{qreg_qubit+1}];\n'''
        measure_qcis = ""
        for qcis_item in qcis_instruction_list:
            if not qcis_item:
                continue
            if qcis_item.startswith('M'):
                measure_qcis += f'{qcis_item}\n'
                continue
            gate = qcis_item.split(' ')[0]
            retrun_qasm = self.get_gate_by_name(gate)(qcis_item)
            qasm += retrun_qasm.__str__()
        measure_gate = GATE_TRANSFORM.get('M')
        qubit_list = self.find_qubit_idx_by_qasm(measure_qcis)
        for idx, qubit_idx in enumerate(qubit_list):
            qasm += f'{measure_gate} q[{int(qubit_idx)}] -> c[{idx}];\n'
        return qasm
