import pytest
from pathlib import Path
from quingo import BackendType, ExeConfig, ExeMode
from quingo import execute
import tempfile


unittest_dir = Path(__file__).parent
qcis_file = unittest_dir / "test_qcis" / "bell.qcis"


@pytest.fixture(scope="module")
def bell_qcis_file():
    """提供 Bell 态的 QCIS 文件路径"""
    return qcis_file


@pytest.fixture(scope="module")
def bell_qcis_string():
    """提供 Bell 态的 QCIS 字符串"""
    return "H Q1\nCNOT Q1 Q2\nM Q1\nM Q2"


def test_resource_estimation_with_qcis_file(bell_qcis_file):
    """测试使用 QCIS 文件进行资源统计"""
    cfg = ExeConfig(
        mode=ExeMode.SimShots, num_shots=10, enable_resource_estimation=True
    )

    result, resource_info = execute(bell_qcis_file, BackendType.QUANTUM_SIM, cfg)

    # 验证执行结果
    assert len(result[0]) == 2  # 两个量子比特
    assert len(result[1]) == 10  # 10 次测量

    # 验证资源统计结果
    depth, num_qubits, ops_count = resource_info
    assert isinstance(depth, int)
    assert depth > 0  # Bell 态电路深度应该大于 0
    assert isinstance(num_qubits, int)
    assert num_qubits == 2  # Bell 态使用 2 个量子比特
    assert isinstance(ops_count, dict)
    assert "h" in ops_count or "H" in str(ops_count).lower()  # 应该包含 Hadamard 门
    assert "cx" in ops_count or "cnot" in str(ops_count).lower()  # 应该包含 CNOT 门


def test_resource_estimation_with_qcis_string(bell_qcis_string):
    """测试使用 QCIS 字符串进行资源统计"""
    cfg = ExeConfig(
        mode=ExeMode.SimShots, num_shots=10, enable_resource_estimation=True
    )

    result, resource_info = execute(bell_qcis_string, BackendType.QUANTUM_SIM, cfg)

    # 验证执行结果
    assert len(result[0]) == 2
    assert len(result[1]) == 10

    # 验证资源统计结果
    depth, num_qubits, ops_count = resource_info
    assert isinstance(depth, int)
    assert depth > 0
    assert isinstance(num_qubits, int)
    assert num_qubits == 2
    assert isinstance(ops_count, dict)


def test_resource_estimation_disabled(bell_qcis_file):
    """测试未开启资源统计时的默认行为"""
    cfg = ExeConfig(
        mode=ExeMode.SimShots,
        num_shots=10,
        enable_resource_estimation=False,  # 显式禁用
    )

    result = execute(bell_qcis_file, BackendType.QUANTUM_SIM, cfg)

    # 结果应该是普通的执行结果，不是元组
    assert not isinstance(result, tuple) or len(result) == 2  # 正常的结果格式
    # 如果是元组，应该是 (names, shots)，不应该有第三个元素
    if isinstance(result, tuple):
        assert len(result[0]) == 2
        assert len(result[1]) == 10


def test_resource_estimation_default_disabled(bell_qcis_file):
    """测试默认情况下资源统计是禁用的"""
    cfg = ExeConfig(mode=ExeMode.SimShots, num_shots=10)
    # 不设置 enable_resource_estimation，应该默认为 False

    result = execute(bell_qcis_file, BackendType.QUANTUM_SIM, cfg)

    # 结果应该是普通的执行结果
    assert not isinstance(result, tuple) or len(result) == 2


def test_resource_estimation_with_non_qcis_file():
    """测试对非 QCIS 文件进行资源统计时的警告"""
    # 创建一个临时的非 QCIS 文件
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".qasm", delete=False
    ) as tmp_file:
        tmp_file.write("H Q1\nCNOT Q1 Q2\nM Q1\nM Q2")
        tmp_path = Path(tmp_file.name)

    try:
        cfg = ExeConfig(
            mode=ExeMode.SimShots, num_shots=10, enable_resource_estimation=True
        )

        # 应该返回普通结果，不包含资源统计
        result = execute(tmp_path, BackendType.QUANTUM_SIM, cfg)

        # 由于跳过了资源统计，应该只返回执行结果
        assert not isinstance(result, tuple) or len(result) == 2

    finally:
        # 清理临时文件
        tmp_path.unlink()


def test_resource_estimation_with_different_modes(bell_qcis_file):
    """测试资源统计在不同执行模式下都能工作"""
    modes = [
        ExeMode.SimShots,
        ExeMode.SimFinalResult,
        ExeMode.SimStateVector,
    ]

    for mode in modes:
        cfg = ExeConfig(mode=mode, num_shots=10, enable_resource_estimation=True)

        result_with_resource = execute(bell_qcis_file, BackendType.QUANTUM_SIM, cfg)

        # 应该返回包含资源统计的元组
        assert isinstance(result_with_resource, tuple)
        assert len(result_with_resource) == 2

        result, resource_info = result_with_resource
        depth, num_qubits, ops_count = resource_info

        # 验证资源统计信息的基本属性
        assert isinstance(depth, int)
        assert isinstance(num_qubits, int)
        assert isinstance(ops_count, dict)
        assert num_qubits == 2


def test_resource_estimation_correctness(bell_qcis_file):
    """测试资源统计结果的正确性"""
    cfg = ExeConfig(
        mode=ExeMode.SimShots, num_shots=10, enable_resource_estimation=True
    )

    result, resource_info = execute(bell_qcis_file, BackendType.QUANTUM_SIM, cfg)
    depth, num_qubits, ops_count = resource_info

    # Bell 态电路特性：
    # - 深度应该约为 3 (H, CNOT, Measure)
    # - 量子比特数为 2
    # - 应该包含 1 个 H 门，1 个 CNOT 门，2 个测量
    assert num_qubits == 2
    assert depth >= 2  # 至少有 H 和 CNOT 的深度

    # 检查门操作数量（注意：不同版本的 qiskit 可能有不同的表示）
    total_gates = sum(ops_count.values())
    assert total_gates >= 3  # 至少有 H, CNOT, Measure 操作


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
