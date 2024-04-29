# 青果运行时系统

青果（Quingo）运行时系统能够与青果编译器协同工作，旨在为用户提供编程和模拟青果程序的能力。

## 环境安装

青果的安装主要包含以下两个步骤：

### 安装运行时系统以及模拟器

依次执行以下命令便可以安装青果运行时系统、`SymQC` 模拟器、`PyQCISim` 模拟器以及 `QuaLeSim` 模拟器。
```sh
pip install -e .
```

```sh
# for simulators used:
# Tequila 后端尚未开源，需要单独安装。
git clone https://gitee.com/hpcl_quanta/tequila.git
pip install -e .
```


### 安装青果编译器

Quingo提供两种方式安装基于`mlir`的青果编译器

+ 执行以下命令便可自动下载安装基于`mlir`的青果编译器：
   ```sh
   python -m quingo.install_quingoc
   ```

+ 从[Quingoc发布地址](https://gitee.com/quingo/quingoc-release/releases)下载基于`mlir`的青果编译器
  + Windows:解压zip压缩包，并将Quingoc所在目录加入到系统环境变量PATH中
  + Linux:执行如下示例命令，Quingoc安装到用户指定的目录，将该目录加入到系统环境变量PATH中
  ```sh
   quingo-compiler-0.1.4.sh -prefix=/home/user/.local
  ```
  + Macos:解压dmg压缩包，将Quingoc可执行文件拷贝到用户指定的目录下，并添加该目录加入到系统环境变量PATH中


## 使用
一个简单的例子可以在目录`src/examples`中找到。您可以通过执行以下命令简单地运行`Bell_state`示例：
```sh
cd src/examples/bell_state
python host.py
```
如果一切正常，将会输出如下结果：
```sh
sim res:  (['Q1', 'Q2'], [[0, 0], [0, 0], [1, 1], [1, 1], [0, 0], [0, 0], [0, 0], [1, 1], [0, 0], [1, 1]])
```
针对不同的模拟后端，详见`src/examples/sim_backend`，其中展示了目前稳定运行的SymQC、QuantumSim何Tequila后端的使用。

针对不同模式的输出格式，详见`src/quingo/backend/quingo_result_format_spec.md`

## 青果运行时系统提供的API
1. `Quingo_task`类:
   - 输入：
      - `called_qu_fn`: `Path`，qu文件路径。
      - `called_func`: `str`，调用 quingo 函数名。
      - `debug_mode`(optional): `True` or `False`。
      - `qisa`(optional): 前端指令集类型。
      - `backend`(optional): 后端模拟器类型。
2. `compile`:
   - 输入：
      - `Quingo_task`: 待编译 qu 任务
      - `params`: `Quingo_task` 中调用函数 `called_func` 所需参数
   - 输出：`qasm_fn`：输出对应指令集文件(.qcis / .qi)
3. `execute`:
   - 输入：
      - `qasm_fn`: `Path`，对应指令集文件(.qcis / .qi)
      - `be_type`: `BackendType`，模拟器后端类型
      - `exe_config`: 执行模式，`ExeMode.SimShots`、`ExeMode.SimFinalResult`、`ExeMode.SimStateVector` 
   - 输出：`sim_result`：具体输出格式详见`src/quingo/backend/quingo_result_format_spec.md`

## 青果示例程序
目前青果运行时系统中已经包含了`Bell_state`、`GHZ`、`VQE`等示例程序，详情可见[此处](https://gitee.com/quingo/quingo-runtime/tree/master/src/examples)。