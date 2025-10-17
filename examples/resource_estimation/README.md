# 量子电路资源估算演示

本目录包含演示如何使用资源估算功能来分析量子电路资源使用情况的示例。

## 功能说明

Quingo Runtime 提供两种方式进行资源估算：

1. **直接调用 `estimate_resource` 函数**：用于独立的资源分析
2. **通过 `execute` 函数**：在执行量子电路的同时获取资源信息

资源估算可以分析 QCIS 格式的量子电路文件，并返回以下信息：

- **电路深度 (Depth)**: 电路在并行执行时所需的最少时间步数
- **量子比特数 (Qubits)**: 电路使用的量子比特数量
- **门操作统计 (Gate Operations)**: 电路中各种量子门的使用次数统计

## 文件说明

- `demo.py`: 主演示脚本，包含三个示例：
  1. 单个电路资源分析（使用 `estimate_resource` 函数）
  2. 多个电路对比分析（使用 `estimate_resource` 函数）
  3. **在 execute 函数中使用资源估算（新增）**

## 前置条件

运行演示脚本前，请确保：

1. 已安装 Quingo Runtime 及其依赖：
   ```bash
   cd /home/xiangfu/quingo-runtime
   pip install -e .
   ```

2. 已编译相关的量子电路示例生成 QCIS 文件：
   ```bash
   # 编译 bell_state 示例
   cd examples/bell_state
   # 使用 quingoc 编译器编译 kernel.qu 生成 QCIS 文件

   # 编译 ghz 示例
   cd examples/ghz
   # 使用 quingoc 编译器编译 kernel.qu 生成 QCIS 文件
   ```

3. 已安装 Qiskit (用于电路转换和分析)：
   ```bash
   pip install qiskit
   ```

## 使用方法

在 quingo-runtime 根目录下运行演示脚本：

```bash
python examples/resource_estimation/demo.py
```

## 示例输出

运行脚本后，您将看到类似如下的输出：

```
======================================================================
  量子电路资源估算演示 (estimate_resource)
======================================================================
======================================================================
示例 1: 分析单个量子电路 (Bell State)
======================================================================

正在分析文件: .../bell_state/build/bell_state.qcis

电路名称: Bell State
----------------------------------------------------------------------
电路深度 (Depth):     3
量子比特数 (Qubits):   2

门操作统计 (Gate Operations):
  measure        :    2
  h              :    1
  cx             :    1
----------------------------------------------------------------------
...
```

## API 使用示例

### 方式 1: 直接使用 estimate_resource 函数

```python
from pathlib import Path
from quingo.lib.qiskit_tools import estimate_resource

# 指定 QCIS 文件路径
qcis_file = Path("path/to/your/circuit.qcis")

# 估算资源
depth, num_qubits, ops_count = estimate_resource(qcis_file)

# 使用结果
print(f"电路深度: {depth}")
print(f"量子比特数: {num_qubits}")
print(f"门操作统计: {dict(ops_count)}")
```

### 方式 2: 通过 execute 函数使用资源估算

```python
from quingo import BackendType, ExeConfig, ExeMode, execute
from pathlib import Path

# 指定 QCIS 文件路径
qcis_file = Path("path/to/your/circuit.qcis")

# 配置执行参数，启用资源估算
config = ExeConfig(
    mode=ExeMode.SimShots,
    num_shots=100,
    enable_resource_estimation=True  # 启用资源估算
)

# 执行并获取结果
result, resource_info = execute(qcis_file, BackendType.QUANTUM_SIM, config)

# 解包资源信息
depth, num_qubits, ops_count = resource_info

# 使用执行结果和资源信息
print(f"执行结果: {result}")
print(f"电路深度: {depth}")
print(f"量子比特数: {num_qubits}")
print(f"门操作统计: {dict(ops_count)}")
```

**优点**：
- 一次调用同时完成量子电路执行和资源估算
- 向后兼容：默认情况下资源估算是关闭的
- 支持所有执行模式（SimShots、SimStateVector、SimFinalResult 等）
- 支持 QCIS 文件和 QCIS 字符串两种输入方式

## 注意事项

- `estimate_resource` 函数会在 QCIS 文件的同目录下生成一个同名的 `.qasm` 文件作为中间转换结果
- 电路深度越小通常意味着算法执行越快，受噪声影响越小
- 双量子比特门（如 CNOT）的数量是评估电路复杂度和错误率的重要指标

## 相关文档

- [Quingo 编程语言文档](https://quingo.xyz)
- [Qiskit 文档](https://qiskit.org/documentation/)

