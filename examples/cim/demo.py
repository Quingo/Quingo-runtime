from pathlib import Path

import numpy as np

from quingo.cim import cim_envolve, read_coupling_graph


def cim_simulate_matrix(couple_matrix: np.ndarray, num_repetitions: int = 3) -> None:
    """
    执行CIM模拟并打印结果

    参数:
        couple_matrix (np.ndarray): 耦合矩阵
        num_repetitions (int): 模拟重复次数,默认3
    """
    print("input matrix: \n", couple_matrix)
    print(f"Simulation result ({num_repetitions} times):")
    for _ in range(num_repetitions):
        sol = cim_envolve(couple_matrix)
        print(sol)
    print("--------------------------------------")


def cim_simulate_coupling_graph(file_path: str, num_repetitions: int = 3) -> None:
    """
    从文件读取耦合图并执行CIM模拟

    参数:
        file_path (str): 耦合图文件路径
        num_repetitions (int): 模拟重复次数,默认3
    """
    couple_matrix = read_coupling_graph(file_path)
    cim_simulate_matrix(couple_matrix, num_repetitions)


if __name__ == "__main__":
    np.set_printoptions(linewidth=200, suppress=True)

    print("========================================================================")
    print("CIM Simulation Example, direct matrix input:")
    print("========================================================================")
    # 输入
    couple_matrix = np.array(
        [
            [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 4],
            [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0],
            [0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0],
            [0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0],
            [0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0],
            [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
            [4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
        ]
    )
    cim_simulate_matrix(couple_matrix)

    couple_matrix = np.array(
        [[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0]]
    )
    cim_simulate_matrix(couple_matrix)

    print("========================================================================")
    print("CIM Simulation Example, read coupling graph from file:")
    print("========================================================================")
    graph_fn = Path(__file__).parent / "coupling_graph.txt"
    cim_simulate_coupling_graph(graph_fn)
