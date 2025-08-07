from pathlib import Path
from typing import Union

import numpy as np


def read_J(coupling_graph_fn: Union[Path, str]) -> np.ndarray:
    """
    从耦合图文件中读取并构建对称的邻接矩阵。

    该函数解析耦合图文件格式，构建一个对称的numpy数组表示图的邻接矩阵。
    文件第一行包含节点数和边数，后续行描述边的连接关系和权重。

    Parameters
    ----------
    coupling_graph_fn : Path or str
        耦合图文件的路径。可以是字符串路径或pathlib.Path对象。

    Returns
    -------
    np.ndarray
        形状为 (num_nodes, num_nodes) 的对称邻接矩阵，其中 J[i,j] 表示
        节点 i 和节点 j 之间的耦合强度。

    Raises
    ------
    ValueError
        如果文件为空、格式错误或边数与声明的边数不匹配。
        具体错误情况包括：
        - 文件内容为空
        - 文件只有一行
        - 第一行格式不正确（不是两个整数）
        - 边的数量与声明的边数不匹配
        - 边的格式不正确（不是三个值：node1 node2 weight）

    Notes
    -----
    文件格式：
    - 第一行：num_nodes num_edges（空格分隔的两个整数）
    - 后续行：node1 node2 weight（空格分隔，其中节点编号从1开始）

    示例文件内容：
        5 4
        1 2 1.0
        2 3 1.0
        3 4 1.0
        4 5 1.0

    该函数会自动将节点编号从1-based转换为0-based，并确保生成的矩阵是对称的。

    Examples
    --------
    >>> J = read_J("coupling_graph.txt")
    >>> print(J.shape)
    (5, 5)
    >>> print(J[0, 1])  # 节点1和节点2之间的耦合
    1.0
    """

    if isinstance(coupling_graph_fn, str):
        coupling_graph_fn = Path(coupling_graph_fn)

    with coupling_graph_fn.open("r") as coupling_graph_file:

        lines = coupling_graph_file.readlines()
        lines = [line.strip() for line in lines if line.strip()]

        if len(lines) == 0:
            raise ValueError("文件内容为空")

        if len(lines) == 1:
            raise ValueError("文件内容格式错误")


        header_info = lines[0].split(' ')

        if len(header_info) != 2:
            raise ValueError("文件内容格式错误")

        num_nodes, num_edges = map(int, header_info)

        if num_edges != len(lines) - 1:
            raise ValueError("文件内容格式错误")

        J = np.zeros((num_nodes, num_nodes))

        edges = lines[1:]
        for edge in edges:
            edge = edge.split(" ")
            if len(edge) != 3:
                raise ValueError("文件内容格式错误")

            node1 = int(edge[0]) - 1
            node2 = int(edge[1]) - 1

            value = float(edge[2])

            J[node1][node2] = value
            J[node2][node1] = value

        return J

def read_coupling_graph(file_path: Union[Path, str]) -> np.ndarray:
    """
    从指定文件路径读取耦合图并返回耦合矩阵

    参数:
        file_path (Path | str): 文件路径,支持字符串或Path对象

    返回:
        np.ndarray: 耦合矩阵,形状为(n_nodes, n_nodes)

    异常:
        FileNotFoundError: 文件不存在
        ValueError: 文件内容格式错误


    说明：
        文件中每一行包含三个元素，分别是 第一个节点、第二个节点、耦合强度
    """
    try:
        return read_J(file_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"文件未找到: {file_path}") from e
    except ValueError as e:
        raise ValueError(f"文件内容格式错误: {str(e)}") from e

def read_plain_matrix(file_path: Union[Path, str]) -> np.ndarray:
    """
    从指定文件路径读取耦合矩阵并返回

    参数:
        file_path (Path | str): 文件路径,支持字符串或Path对象

    返回:
        np.ndarray: 耦合矩阵,形状为(n_nodes, n_nodes)

    异常:
        FileNotFoundError: 文件不存在
        ValueError: 文件内容格式错误

    文件格式说明：
        文件中包含一个 n x n 的矩阵，每一行包含 n 个元素，表示矩阵的每一行
        例如：
            0 1 0 0 0
            1 0 1 0 0
            0 1 0 1 0
            0 0 1 0 1
            0 0 0 1 0
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"文件未找到: {file_path}")

    with file_path.open("r") as file:
        lines = file.readlines()
        matrix = np.array([line.split() for line in lines], dtype=float)
        return matrix

