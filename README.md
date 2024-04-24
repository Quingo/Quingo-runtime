# Quingo Runtime System

Along with quingo compilers, the Quingo runtime system which provides users the capability to program and simulate Quingo programs.

## Installation

The Quingo installation comprises of two main steps:

### Install the Runtime system and simulator
Install Quingo runtime system with required simulators using the following command:
```sh
pip install -e .
```

```sh
# for simulators used:
# The Tequila backend is not yet open source and needs to be installed separately.
git clone https://gitee.com/hpcl_quanta/tequila.git
pip install -e .
```

Upon success, it will automatically install the Quingo runtime system (this package), the SymQC simulator, the PyQCISim simulator and the QuaLeSim simulator.

### Install the Quingo compiler

We can install mlir-based quingo compiler in two ways:

+ Install the mlir-based Quingo compiler using the following command:
  ```sh
  python -m quingo.install_quingoc
  ```

+ Download [mlir-based Quingo compiler](https://gitee.com/quingo/quingoc-release/releases)
  + Windows: unzip .zip file, add directory which contains the quingoc executable file to system environment PATH.
  + Linux: as the following sample usage, Quingoc will be installed to user defined directory, then add directory which contains the quingoc executable file to system environment PATH.
  ```sh
   quingo-compiler-0.1.4.sh -prefix=/home/user/.local
  ```
  + Macos: uncompress .dmg file, copy quingoc executable file to user defined directory, then add directory which contains the quingoc executable file to system environment PATH.


## Usage
A simple example can be found in the directory `src/examples`. You can simply run the bell_state example by running:
```sh
cd src/examples/bell_state
python host.py
```
If everything runs correctly, you should see the following output:
```sh
sim res:  (['Q1', 'Q2'], [[0, 0], [0, 0], [1, 1], [1, 1], [0, 0], [0, 0], [0, 0], [1, 1], [0, 0], [1, 1]])
```
For different simulation backend, please refer to `src/examples/sim_backend`, which shows the use of SymQC, QuantumSim, and Tequila backend that are currently running stably.

For different simulation modes, please refer to `src/examples/sim_exemode`, which displays the output of two different simulation results currently available.

## APIs of the Quingo runtime system
1. `class Quingo_task`:
   - 输入：
      - `called_qu_fn`: `Path`，qu文件路径。
      - `called_func`: `str`，调用 quingo 函数名。
      - `debug_mode`(optional): `True` or `False`。
      - `qisa`(optional): 前端指令集类型。
      - `backend`(optional): 后端模拟器类型。
2. `function compile()`:
   - 输入：
      - `Quingo_task`: 待编译 qu 任务
      - `params`: `Quingo_task` 中调用函数 `called_func` 所需参数
   - 输出：`qasm_fn`：输出对应指令集文件(.qcis / .qi)
3. `function execute()`:
   - 输入：
      - `qasm_fn`: `Path`，对应指令集文件(.qcis / .qi)
      - `be_type`: `BackendType`，模拟器后端类型
      - `exe_config`: 执行模式，`ExeMode.SimShots`、`ExeMode.SimFinalResult`、`ExeMode.SimStateVector` 
   - 输出：`sim_result`：具体输出格式详见`src/quingo/backend/quingo_result_format_spec.md`

## Quingo programming tutorial
At present, Qingguo runtime system has included sample programs such as `Bell_state`, `GHZ`, `VQE`, etc. Details can be found [here](https://gitee.com/quingo/quingo-runtime/tree/master/src/examples).