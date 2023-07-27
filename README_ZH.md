# 青果运行时系统

青果（Quingo）运行时系统能够与青果编译器协同工作，旨在为用户提供编程和模拟青果程序的能力。

## 环境安装

青果的安装主要包含以下两个步骤：

### 安装运行时系统以及模拟器

依次执行以下命令便可以安装青果运行时系统、PyQCAS模拟器以及PyQCISim模拟器。
```sh
pip install quingo
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

## 青果示例程序
目前青果运行时系统中已经包含了`Bell_state`、`GHZ`、`VQE`等示例程序，详情可见[此处](https://gitee.com/quingo/quingo-runtime/tree/master/src/examples)。