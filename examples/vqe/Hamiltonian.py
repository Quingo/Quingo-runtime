import numpy as np
from numpy import *
from expand_gate import expand_gate


class Hamiltonian:
    def __init__(self, paulis, coeffs):
        self.paulis = paulis
        self.coeffs = coeffs
        assert len(paulis) == len(coeffs)
        self.num_qubits = len(paulis[0])
        self.num_paulis = len(paulis)

    def __str__(self):
        s = ""
        for i in range(self.num_paulis):
            s += str(self.coeffs[i]) + "*" + str(self.paulis[i]) + " + "
        return s[:-3]

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return self.num_paulis

    def __getitem__(self, i):
        return self.paulis[i], self.coeffs[i]

    def __iter__(self):
        return iter(zip(self.paulis, self.coeffs))

    def to_matrix(self):
        """
        paulis: list of Pauli matrices,
                e.g. ["X", "Y", "Z", ...] for 1-qubit Paulis
                e.g. ["XI", "IZ", "ZZ", ...] for 2-qubit Paulis
                e.g. ["XIZI", "IZZI", "ZZZZ", ...] for 4-qubit Paulis
        coeffs: list of coefficients,
                e.g. [1.0, -0.5, 0.3, ...] and len(coeffs) == len(paulis)
        for example,
        the Hamiltonian H = g0*I + g1*Z0 + g2*Z1 + g3*Z0Z1 + g4*Y0Y1 + g5*X0X1
        can be represented as
        paulis = ["II", "IZ", "ZI", "ZZ", "YY", "XX"]
        coeffs = [g0, g1, g2, g3, g4, g5]
        """
        X = pauli_gate(1)
        Y = pauli_gate(2)
        Z = pauli_gate(3)
        I = pauli_gate(4)

        sigmas = []
        for i in range(self.num_paulis):
            assert len(self.paulis[i]) == self.num_qubits
            s = eye(2**self.num_qubits)
            for j in range(self.num_qubits):
                if str(self.paulis[i][j]) == "I":
                    s = s * expand_gate(self.num_qubits, I, [j])
                elif str(self.paulis[i][j]) == "X":
                    s = s * expand_gate(self.num_qubits, X, [j])
                elif str(self.paulis[i][j]) == "Y":
                    s = s * expand_gate(self.num_qubits, Y, [j])
                elif str(self.paulis[i][j]) == "Z":
                    s = s * expand_gate(self.num_qubits, Z, [j])
                else:
                    raise ValueError("Invalid Pauli string")
            sigmas.append(s)
        assert len(sigmas) == self.num_paulis
        h = np.zeros(sigmas[0].shape)
        for i in range(len(sigmas)):
            h = h + self.coeffs[i] * sigmas[i]
        return h


def pauli_gate(i):
    if i == 1:
        m = np.matrix([[0, 1], [1, 0]])
    elif i == 2:
        m = np.matrix([[0, -1j], [1j, 0]])
    elif i == 3:
        m = np.matrix([[1, 0], [0, -1]])
    elif i == 4:
        m = np.matrix([[1, 0], [0, 1]])
    else:
        raise IndexError("Invalid Pauli index")
    return m


def hamiltonian(paulis, coeffs):
    """
    paulis: list of Pauli matrices,
            e.g. ["X", "Y", "Z", ...] for 1-qubit Paulis
            e.g. ["XI", "IZ", "ZZ", ...] for 2-qubit Paulis
            e.g. ["XIZI", "IZZI", "ZZZZ", ...] for 4-qubit Paulis
    coeffs: list of coefficients,
            e.g. [1.0, -0.5, 0.3, ...] and len(coeffs) == len(paulis)
    for example,
    the Hamiltonian H = g0*I + g1*Z0 + g2*Z1 + g3*Z0Z1 + g4*Y0Y1 + g5*X0X1
    can be represented as
    paulis = ["II", "IZ", "ZI", "ZZ", "YY", "XX"]
    coeffs = [g0, g1, g2, g3, g4, g5]
    """
    X = pauli_gate(1)
    Y = pauli_gate(2)
    Z = pauli_gate(3)
    I = pauli_gate(4)

    assert len(coeffs) == len(paulis)
    sigmas = []
    for i in range(len(paulis)):
        assert len(paulis[i]) == len(paulis[0])
        s = eye(2 ** len(paulis[i]))
        for j in range(len(paulis[i])):
            if str(paulis[i][j]) == "I":
                s = s * expand_gate(len(paulis[i]), I, [j])
            elif str(paulis[i][j]) == "X":
                s = s * expand_gate(len(paulis[i]), X, [j])
            elif str(paulis[i][j]) == "Y":
                s = s * expand_gate(len(paulis[i]), Y, [j])
            elif str(paulis[i][j]) == "Z":
                s = s * expand_gate(len(paulis[i]), Z, [j])
            else:
                raise ValueError("Invalid Pauli string")
        sigmas.append(s)
    assert len(sigmas) == len(paulis)
    h = np.zeros(sigmas[0].shape)
    for i in range(len(sigmas)):
        h = h + coeffs[i] * sigmas[i]
    return h


# def expand_1q_gate(gate, target_qubit):
#     """Expand a single-qubit gate applied on the `target_qubit` to a 4 x 4 matrix.
#     Qubits in the basis is organized as: |qubit_1, qubit_0>
#     The basis of this matrix is shown as following:
#          |00>  |01>  |10>  |11>
#     |00>  xx    xx    xx    xx
#     |01>  xx    xx    xx    xx
#     |10>  xx    xx    xx    xx
#     |11>  xx    xx    xx    xx
#     """
#     if target_qubit == 1:
#         return np.kron(gate, eye(2))
#     elif target_qubit == 0:
#         return np.kron(eye(2), gate)
#     else:
#         raise ValueError(
#             "Given target_qubit ({}) is neither 0 or 1.".format(target_qubit)
#         )


# def gate(i):
#     if i == 1:
#         m = np.matrix([[0, 1], [1, 0]])
#     elif i == 2:
#         m = np.matrix([[0, -1j], [1j, 0]])
#     elif i == 3:
#         m = np.matrix([[1, 0], [0, -1]])
#     elif i == 4:
#         m = np.matrix([[1, 0], [0, 1]])
#     else:
#         raise IndexError("Invalid Pauli index")
#     return m


# def hamiltonian2(g):
#     """Generate the hamiltonian for the H2 molecule, which is:
#     H = g0*I + g1*Z0 + g2*Z1 + g3*Z0Z1 + g4*Y0Y1 + g5*X0X1
#     """
#     X = gate(1)
#     Y = gate(2)
#     Z = gate(3)

#     assert len(g) == 6
#     sigmas = [
#         eye(4),
#         expand_1q_gate(Z, 0),
#         expand_1q_gate(Z, 1),
#         expand_1q_gate(Z, 0) * expand_1q_gate(Z, 1),
#         expand_1q_gate(X, 0) * expand_1q_gate(X, 1),
#         expand_1q_gate(Y, 0) * expand_1q_gate(Y, 1),
#     ]
#     h = zeros((4, 4))
#     for i in range(6):
#         h = h + np.dot(g[i], sigmas[i])

#     return h

# from qiskit.quantum_info import SparsePauliOp

# H2_op = SparsePauliOp.from_list(
#     [
#         ("II", -1.052373245772859),
#         ("IZ", 0.39793742484318045),
#         ("ZI", -0.39793742484318045),
#         ("ZZ", -0.01128010425623538),
#         ("XX", 0.18093119978423156),
#     ]
# )
# print(hamiltonian(H2_op.paulis, H2_op.coeffs))
