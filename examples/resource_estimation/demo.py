"""量子电路资源估算演示

本脚本演示如何使用资源估算功能来分析量子电路的资源使用情况，包括电路深度、量子比特数和门操作统计。

提供两种方式：
1. 直接使用 quingo.lib.qiskit_tools.estimate_resource 函数
2. 通过 execute 函数的 ExeConfig 配置启用资源估算
"""

from pathlib import Path
from quingo.lib.qiskit_tools import estimate_resource
from quingo import BackendType, ExeConfig, ExeMode, execute


def print_separator(char="=", length=70):
    """打印分隔线"""
    print(char * length)


def print_resource_info(circuit_name, depth, num_qubits, ops_count):
    """
    格式化打印电路资源信息

    Parameters
    ----------
    circuit_name : str
        电路名称
    depth : int
        电路深度
    num_qubits : int
        量子比特数
    ops_count : OrderedDict
        门操作统计
    """
    print(f"\n电路名称: {circuit_name}")
    print_separator("-")
    print(f"电路深度 (Depth):     {depth}")
    print(f"量子比特数 (Qubits):   {num_qubits}")
    print(f"\n门操作统计 (Gate Operations):")
    for gate_name, count in ops_count.items():
        print(f"  {gate_name:15s}: {count:4d}")
    print_separator("-")


def demo_single_circuit():
    """演示：分析单个量子电路的资源使用"""
    print_separator()
    print("示例 1: 分析单个量子电路 (Bell State)")
    print_separator()

    # 定义 QCIS 文件路径
    # Bell State 是一个简单的两量子比特纠缠态电路
    bell_qcis = Path(__file__).parent.parent / "bell_state/build/bell_state.qcis"

    # 检查文件是否存在
    if not bell_qcis.exists():
        print(f"错误: QCIS 文件不存在: {bell_qcis}")
        print("请先编译 bell_state 示例以生成 QCIS 文件")
        return

    print(f"\n正在分析文件: {bell_qcis}")

    # 调用 estimate_resource 函数进行资源估算
    # 返回值为一个包含三个元素的元组：
    #   - depth: 电路深度
    #   - num_qubits: 量子比特数
    #   - ops_count: 门操作统计（OrderedDict）
    depth, num_qubits, ops_count = estimate_resource(bell_qcis)

    # 打印结果
    print_resource_info("Bell State", depth, num_qubits, ops_count)

    # 解释结果
    print("\n结果解释:")
    print("- 电路深度表示并行执行时所需的最少时间步数")
    print("- 量子比特数表示电路使用的量子资源数量")
    print("- 门操作统计显示了各种量子门的使用次数")


def demo_multiple_circuits_comparison():
    """演示：对比多个量子电路的资源使用"""
    print_separator()
    print("示例 2: 对比多个量子电路的资源使用")
    print_separator()

    # 定义要对比的电路
    circuits = [
        {
            "name": "Bell State",
            "path": Path(__file__).parent.parent / "bell_state/build/bell_state.qcis",
            "description": "两量子比特纠缠态",
        },
        {
            "name": "GHZ State",
            "path": Path(__file__).parent.parent / "ghz/build/ghz.qcis",
            "description": "多量子比特GHZ态",
        },
    ]

    # 收集所有电路的资源信息
    results = []
    for circuit in circuits:
        if not circuit["path"].exists():
            print(f"\n警告: 跳过 {circuit['name']} - 文件不存在: {circuit['path']}")
            continue

        depth, num_qubits, ops_count = estimate_resource(circuit["path"])
        results.append(
            {
                "name": circuit["name"],
                "description": circuit["description"],
                "depth": depth,
                "num_qubits": num_qubits,
                "ops_count": ops_count,
                "total_gates": sum(ops_count.values()),
            }
        )

    # 以表格形式打印对比结果
    if results:
        print("\n" + "=" * 90)
        print(
            f"{'电路名称':<20} {'描述':<20} {'深度':<8} {'量子比特':<10} {'总门数':<10}"
        )
        print("=" * 90)
        for result in results:
            print(
                f"{result['name']:<20} {result['description']:<20} "
                f"{result['depth']:<8} {result['num_qubits']:<10} {result['total_gates']:<10}"
            )
        print("=" * 90)

        # 打印每个电路的详细门操作统计
        print("\n详细门操作统计:")
        for result in results:
            print_resource_info(
                result["name"],
                result["depth"],
                result["num_qubits"],
                result["ops_count"],
            )


def demo_execute_with_resource_estimation():
    """演示：通过 execute 函数使用资源估算"""
    print_separator()
    print("示例 3: 在 execute 函数中使用资源估算")
    print_separator()

    # 定义 QCIS 文件路径
    bell_qcis = Path(__file__).parent.parent / "bell_state/build/bell_state.qcis"

    # 检查文件是否存在
    if not bell_qcis.exists():
        print(f"错误: QCIS 文件不存在: {bell_qcis}")
        print("请先编译 bell_state 示例以生成 QCIS 文件")
        return

    print(f"\n正在执行文件: {bell_qcis}")
    print("\n方法 1: 不启用资源估算（默认行为）")
    print("-" * 70)

    # 方法 1: 默认执行，不进行资源估算
    cfg_no_resource = ExeConfig(
        mode=ExeMode.SimShots,
        num_shots=10,
        enable_resource_estimation=False,  # 默认值，可以省略
    )

    result = execute(bell_qcis, BackendType.QUANTUM_SIM, cfg_no_resource)
    print(f"执行结果: {result}")
    print(f"结果类型: 普通执行结果")

    print("\n方法 2: 启用资源估算")
    print("-" * 70)

    # 方法 2: 启用资源估算
    cfg_with_resource = ExeConfig(
        mode=ExeMode.SimShots,
        num_shots=10,
        enable_resource_estimation=True,  # 启用资源估算
    )

    result_with_resource = execute(
        bell_qcis, BackendType.QUANTUM_SIM, cfg_with_resource
    )

    # 解包结果
    execution_result, resource_info = result_with_resource
    depth, num_qubits, ops_count = resource_info

    print(f"执行结果: {execution_result}")
    print(f"\n资源估算信息:")
    print_resource_info("Bell State", depth, num_qubits, ops_count)

    print("\n方法 3: 使用 QCIS 字符串执行并估算资源")
    print("-" * 70)

    # 方法 3: 直接使用 QCIS 字符串
    qcis_string = "H Q1\nCNOT Q1 Q2\nM Q1\nM Q2"

    cfg_string = ExeConfig(
        mode=ExeMode.SimShots, num_shots=5, enable_resource_estimation=True
    )

    result_str, resource_str = execute(qcis_string, BackendType.QUANTUM_SIM, cfg_string)
    depth_str, num_qubits_str, ops_count_str = resource_str

    print(f"执行结果: {result_str}")
    print(f"\n资源估算信息:")
    print_resource_info(
        "Bell State (from string)", depth_str, num_qubits_str, ops_count_str
    )

    print("\n使用建议:")
    print("-" * 70)
    print("1. 默认情况下，资源估算是关闭的，不会影响性能")
    print("2. 需要资源统计时，设置 enable_resource_estimation=True")
    print("3. 资源估算仅支持 QCIS 格式的量子电路")
    print("4. 返回的资源信息包括：电路深度、量子比特数、门操作统计")
    print("5. 资源估算在所有执行模式下都可用（SimShots、SimStateVector 等）")


def main():
    """主函数：运行所有演示"""
    print("\n")
    print("=" * 70)
    print("  量子电路资源估算演示")
    print("=" * 70)

    # 示例 1: 单个电路分析
    demo_single_circuit()

    print("\n\n")

    # 示例 2: 多电路对比
    demo_multiple_circuits_comparison()

    print("\n\n")

    # 示例 3: 在 execute 函数中使用资源估算
    demo_execute_with_resource_estimation()

    print("\n\n")

    print("\n")
    print_separator()
    print("演示完成！")
    print_separator()
    print("\n")


if __name__ == "__main__":
    main()
