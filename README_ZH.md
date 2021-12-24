# 青果运行时系统

 青果（Quingo）运行时系统能够与青果编译器协同工作，旨在为用户提供编程和模拟青果程序的能力。

## 环境安装


### 概述
青果的安装主要包含以下两个步骤：


#### 安装运行时系统以及模拟器

使用以下命令便可以一键安装青果运行时系统、PyQCAS模拟器以及PyQCISim模拟器。
```sh
pip install quingo
```


#### 青果编译器

由于青果运行时系统是一个集成和管理量子和经典计算资源的框架，因此默认情况下它是不包含量子编译器，故青果编译器需要单独下载。

目前的青果编译器有两个版本：

1. 基于`xtext`的青果编译器，通过下载[java二进制文件](https://github.com/Quingo/compiler_xtext/releases)即可获取。
2. 基于`mlir`的青果编译器，通过下载[二进制文件](https://gitee.com/hpcl_quanta/quingo-runtime/releases)即可获取。

基于`xtex`的青果编译器可以生成能够被PyQCAS模拟器模拟的eQASM指令，而基于`mlir`的青果编译器目前能够生成可以被PyQCISim模拟器模拟的 QCIS指令。

下载二进制文件后，需使用以下命令来指定编译器的路径：
```python
import quingo
# xtext编译器
quingo.quingo_interface.set_xtext_compiler_path(<path-to-quingo.jar>)
# mlir编译器
quingo.quingo_interface.set_mlir_compiler_path(<path-to-quingoc>)
```

对于mlir青果编译器，也可以将其二进制文件放在一个指定的目录，以便您的终端可以找到它，例如`/usr/local/bin/`。在这种情况下，便不再需要调用 `set_mlir_compiler_path` 来指定编译器的路径。

### Linux系统下的注意事项
由于编译器的可执行文件（`quinoc`）依赖于Linux系统中的许多库，如果你仅下载编译器的可执行二进制文件，`quinoc` 可能无法正常工作。为了解决在Linux系统下运行青果程序的困难，我们准备了一个docker镜像（大小大约在400MB左右），该镜像将所需的环境一并打包，无需额外安装便可以运行青果程序。使用以下命令可以快速安装：
```sh
docker pull xsu1989/quingo:beta
docker run -it xsu1989/quingo:beta
cd examples && python3 host.py
```


## 使用
一个简单的例子可以在目录`src/examples`中找到。您可以通过运行以下命令简单地运行`bell_state`示例：
```sh
cd src/examples/bell_state
python host.py
```
如果一切正常，将会有以下输出结果：
```sh
connecting pyqcisim_quantumsim...
num_qubits:  2
The result of bell_state is:
(['q0', 'q1'], {'00': 504, '01': 0, '10': 0, '11': 496})
```

## 青果运行时系统提供的API
`Quingo_interface`类提供了以下方法:
 - `set_log_level(<log_level>)`: 该方法中`<log_level>`的值可以是`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`中的任意一个。
 - `connect_backend(<backend>)`: 该方法中`<backend>`的值目前可以是`'pyqcas_quantumsim'`或者`'pyqcisim_quantumsim'`。
- `get_backend_name()`方法返回正在使用的后端名称。如果没有设置后端，将返回一个空字符串。
- `set_compiler(<compiler_name>)`: `<compiler_name>`中的值可以是`'mlir'` 或者`'xtext'`。
- `get_last_qasm()`用来获取上次执行生成的qasm指令代码。
- `config_execution(<mode>, <num_shots>)`:
  -  `config_execution`能够将执行模式配置为`'one_shot'`或`'state_vector'`.
  -  当执行模式为`'one_shot'`时，可以同时使用参数`num_shots`来配置量子线路的运行次数。
-  `call_quingo(<qg_filename>, <qg_func_name>, *args)`:
   - `call_quingo`方法是调用Quingo操作的主要入口。
   - `<qg_filename (str)>`中的值为青果文件的名称，该青果文件中包含被宿主程序调用的量子操作。
   - `<qg_func_name (str)>`中的值为量子操作的名称。
   - `<args (dict)>`中的值为可变长度的参数，这些参数用来以 `qg_func_name(<args>)` 形式来调用青果操作。
- `read_result()`方法负责从量子内核中读取计算结果。
   - 对于能够执行eQASM指令的后端，结果是对量子计算结果进行编码的二进制块。
   - 对于能够执行QCIS指令的后端，结果的格式由PyQCISim进行定义。详情请参考`quingo.if_backend.non_arch_backend.pyqcisim_quantumsim.PyQCISim_quantumsim::execute()`中的文档描述。

## 青果程序示例
持续更新中...