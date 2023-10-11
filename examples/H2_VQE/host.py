import logging
from quingo import *
from pathlib import Path
import matplotlib.pyplot as plt
# from scipy.optimize import minimize_scalar, minimize
from scipy.optimize import minimize_scalar
from numpy import *
import numpy as np

cfg = ExeConfig(ExeMode.SimStateVector,10)

qu_file = Path(__file__).parent / "kernel.qu"

bond_h_decompose = [
    [0.20,  2.8489, 0.5678, -1.4508, 0.6799, 0.0791, 0.0791],
    [0.25,  2.1868, 0.5449, -1.2870, 0.6719, 0.0798, 0.0798],
    [0.30,  1.7252, 0.5215, -1.1458, 0.6631, 0.0806, 0.0806],
    [0.35,  1.3827, 0.4982, -1.0226, 0.6537, 0.0815, 0.0815],
    [0.40,  1.1182, 0.4754, -0.9145, 0.6438, 0.0825, 0.0825],
    [0.45,  0.9083, 0.4534, -0.8194, 0.6336, 0.0835, 0.0835],
    [0.50,  0.7381, 0.4325, -0.7355, 0.6233, 0.0846, 0.0846],
    [0.55,  0.5979, 0.4125, -0.6612, 0.6129, 0.0858, 0.0858],
    [0.60,  0.4808, 0.3937, -0.5950, 0.6025, 0.0870, 0.0870],
    [0.65,  0.3819, 0.3760, -0.5358, 0.5921, 0.0883, 0.0883],
    [0.70,  0.2976, 0.3593, -0.4826, 0.5818, 0.0896, 0.0896],
    [0.75,  0.2252, 0.3435, -0.4347, 0.5716, 0.0910, 0.0910],
    [0.80,  0.1626, 0.3288, -0.3915, 0.5616, 0.0925, 0.0925],
    [0.85,  0.1083, 0.3149, -0.3523, 0.5518, 0.0939, 0.0939],
    [0.90,  0.0609, 0.3018, -0.3168, 0.5421, 0.0954, 0.0954],
    [0.95,  0.0193, 0.2895, -0.2845, 0.5327, 0.0970, 0.0970],
    [1.00, -0.0172, 0.2779, -0.2550, 0.5235, 0.0986, 0.0986],
    [1.05, -0.0493, 0.2669, -0.2282, 0.5146, 0.1002, 0.1002],
    [1.10, -0.0778, 0.2565, -0.2036, 0.5059, 0.1018, 0.1018],
    [1.15, -0.1029, 0.2467, -0.1810, 0.4974, 0.1034, 0.1034],
    [1.20, -0.1253, 0.2374, -0.1603, 0.4892, 0.1050, 0.1050],
    [1.25, -0.1452, 0.2286, -0.1413, 0.4812, 0.1067, 0.1067],
    [1.30, -0.1629, 0.2203, -0.1238, 0.4735, 0.1083, 0.1083],
    [1.35, -0.1786, 0.2123, -0.1077, 0.4660, 0.1100, 0.1100],
    [1.40, -0.1927, 0.2048, -0.0929, 0.4588, 0.1116, 0.1116],
    [1.45, -0.2053, 0.1976, -0.0792, 0.4518, 0.1133, 0.1133],
    [1.50, -0.2165, 0.1908, -0.0666, 0.4451, 0.1149, 0.1149],
    [1.55, -0.2265, 0.1843, -0.0549, 0.4386, 0.1165, 0.1165],
    [1.60, -0.2355, 0.1782, -0.0442, 0.4323, 0.1181, 0.1181],
    [1.65, -0.2436, 0.1723, -0.0342, 0.4262, 0.1196, 0.1196],
    [1.70, -0.2508, 0.1667, -0.0251, 0.4204, 0.1211, 0.1211],
    [1.75, -0.2573, 0.1615, -0.0166, 0.4148, 0.1226, 0.1226],
    [1.80, -0.2632, 0.1565, -0.0088, 0.4094, 0.1241, 0.1241],
    [1.85, -0.2684, 0.1517, -0.0015, 0.4042, 0.1256, 0.1256],
    [1.90, -0.2731, 0.1472,  0.0052, 0.3992, 0.1270, 0.1270],
    [1.95, -0.2774, 0.1430,  0.0114, 0.3944, 0.1284, 0.1284],
    [2.00, -0.2812, 0.1390,  0.0171, 0.3898, 0.1297, 0.1297],
    [2.05, -0.2847, 0.1352,  0.0223, 0.3853, 0.1310, 0.1310],
    [2.10, -0.2879, 0.1316,  0.0272, 0.3811, 0.1323, 0.1323],
    [2.15, -0.2908, 0.1282,  0.0317, 0.3769, 0.1335, 0.1335],
    [2.20, -0.2934, 0.1251,  0.0359, 0.3730, 0.1347, 0.1347],
    [2.25, -0.2958, 0.1221,  0.0397, 0.3692, 0.1359, 0.1359],
    [2.30, -0.2980, 0.1193,  0.0432, 0.3655, 0.1370, 0.1370],
    [2.35, -0.3000, 0.1167,  0.0465, 0.3620, 0.1381, 0.1381],
    [2.40, -0.3018, 0.1142,  0.0495, 0.3586, 0.1392, 0.1392],
    [2.45, -0.3035, 0.1119,  0.0523, 0.3553, 0.1402, 0.1402],
    [2.50, -0.3051, 0.1098,  0.0549, 0.3521, 0.1412, 0.1412],
    [2.55, -0.3066, 0.1078,  0.0572, 0.3491, 0.1422, 0.1422],
    [2.60, -0.3079, 0.1059,  0.0594, 0.3461, 0.1432, 0.1432],
    [2.65, -0.3092, 0.1042,  0.0614, 0.3433, 0.1441, 0.1441],
    [2.70, -0.3104, 0.1026,  0.0632, 0.3406, 0.1450, 0.1450],
    [2.75, -0.3115, 0.1011,  0.0649, 0.3379, 0.1458, 0.1458],
    [2.80, -0.3125, 0.0997,  0.0665, 0.3354, 0.1467, 0.1467],
    [2.85, -0.3135, 0.0984,  0.0679, 0.3329, 0.1475, 0.1475]]


def gate(i):
    if i == 1:
        m = np.mat("0, 1; 1, 0")
    elif i == 2:
        m = np.mat("0, -1j; 1j, 0")
    elif i == 3:
        m = np.mat("1, 0; 0, -1")
    else:
        raise IndexError("Invalid Pauli index")
    return m


def expand_1q_gate(gate, target_qubit):
    '''Expand a single-qubit gate applied on the `target_qubit` to a 4 x 4 matrix.
    Qubits in the basis is organized as: |qubit_1, qubit_0>
    The basis of this matrix is shown as following:
         |00>  |01>  |10>  |11>
    |00>  xx    xx    xx    xx
    |01>  xx    xx    xx    xx
    |10>  xx    xx    xx    xx
    |11>  xx    xx    xx    xx
    '''
    if target_qubit == 1:
        return np.kron(gate, eye(2))
    elif target_qubit == 0:
        return np.kron(eye(2), gate)
    else:
        raise ValueError(
            "Given target_qubit ({}) is neither 0 or 1.".format(target_qubit))


def hamiltonian(g):
    '''Generate the hamiltonian for the H2 molecule, which is:
        H = g0*I + g1*Z0 + g2*Z1 + g3*Z0Z1 + g4*Y0Y1 + g5*X0X1
    '''
    X = gate(1)
    Y = gate(2)
    Z = gate(3)

    assert(len(g) == 6)
    sigmas = [eye(4),
              expand_1q_gate(Z, 0),
              expand_1q_gate(Z, 1),
              expand_1q_gate(Z, 0) * expand_1q_gate(Z, 1),
              expand_1q_gate(X, 0) * expand_1q_gate(X, 1),
              expand_1q_gate(Y, 0) * expand_1q_gate(Y, 1)]
    h = zeros((4, 4))
    for i in range(6):
        h = h + np.dot(g[i], sigmas[i])

    return h


def get_ansatz(circ_name, theta):
    task = Quingo_task(qu_file, circ_name)
    #res = call(task, (theta,), BackendType.DQCSIM_TEQUILA, cfg,config_fn="./std_qcis.qfg")
    qasm_fn = compile(task, (theta,),config_file="./std_qcis.qfg")
    res = execute(qasm_fn, BackendType.DQCSIM_QUANTUMSIM, cfg)
    print([i for i in res["quantum"][1]])
    res = execute(qasm_fn, BackendType.DQCSIM_TEQUILA, cfg)
    print([i for i in res["quantum"][1]])
    res = execute(qasm_fn, BackendType.SYMQC, cfg)
    print([i.evalf() for i in res["quantum"][1]])
    return res


def get_real(c):
    return np.real(c)


def expectation(h, state):
    ''' Return the expectation value of the given state under the given hamiltonian.
    '''
    state_matrix = np.mat(state).T
    t_conj_state = state_matrix.T.conjugate()
    return get_real(np.dot(t_conj_state, np.dot(h, state_matrix)))


def energy_theta(theta: np.double, g):
    '''Return the calculated energy for the given parameter theta.
    '''
    ansatz_state = get_ansatz("ansatz", theta)
    h = hamiltonian(g)
    energy = expectation(h, ansatz_state)
    return energy


def eval_all():
    bond_length = []
    lowest_energies = []
    # theta = -np.pi/2
    for b in bond_h_decompose:
        bond_length.append(b[0])
        g = b[1:]

        # --------------- brute-force scanning - --------------
        # angles = np.linspace(-np.pi/2, np.pi/2, 50)
        # tmp_lowest_energies = [energy_theta(theta, g) for theta in angles]
        # ele_tmp_lowest_energies = (min(tmp_lowest_energies)).A[0][0]
        # lowest_energies.append(ele_tmp_lowest_energies)

        # # --------------- optimization based on searching ---------------
        minimum = minimize_scalar(
            lambda theta: (energy_theta(theta, g)).A[0][0])
        lowest_energies.append(minimum.fun)

    plt.plot(bond_length, lowest_energies, "b.-")
    plt.xlabel("Bond Length")
    plt.title("Variational Quantum Eigensolver")
    plt.ylabel("Energy")
    plt.show()


#eval_all()
get_ansatz("ansatz", 0.0)