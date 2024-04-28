"""Visualization functions for quantum circuits.

Note, this module requires qiskit to be installed.
"""

from qiskit import QuantumCircuit
from pathlib import Path
from pyqcisim.qcis_to_openqasm import qcis_file_2_qasm_file


def qcis_2_qiskit_qc(qcis_fn: Path):
    """Convert a QCIS file to a qiskit QuantumCircuit object."""
    qasm_fn = qcis_fn.with_suffix(".qasm")
    qasm_str = qcis_file_2_qasm_file(qcis_fn, qasm_fn)
    return QuantumCircuit.from_qasm_file(str(qasm_fn))


def draw_circ(qcis_fn: Path, output="mpl"):
    """Draw the quantum circuit using qiskit.
    Use the output parameter to choose the drawing format:

        **text**: ASCII art TextDrawing that can be printed in the console.

        **mpl**: images with color rendered purely in Python using matplotlib.

        **latex**: high-quality images compiled via latex.

        **latex_source**: raw uncompiled latex output.
    """
    qasm_fn = qcis_fn.with_suffix(".qasm")
    qasm_str = qcis_file_2_qasm_file(qcis_fn, qasm_fn)
    qc = QuantumCircuit.from_qasm_file(str(qasm_fn))
    return qc.draw(output=output)
