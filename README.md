# Quingo Runtime System

Along with quingo compilers, the Quingo runtime system which provides users the capability to program and simulate Quingo programs.

## Installation


### Overview
The Quingo installation comprises of two main steps:

#### Runtime system and simulator
Install Quingo runtime system with required simulators using the following command:
```sh
pip install quingo
```

Upon success, it will automatically install the Quingo runtime system (this package), the PyQCAS simulator and the PyQCISim simulator.

#### The Quingo compiler
Since the Quingo runtime is a framework integrating and managing quantum and classical computational resources, it does not contain the quantum compiler by default. The Quingo compiler should be downloaded separately.

Two versions of Quingo compiler has been developed:
1. the xtext-based compiler, which appears as a [java executable](https://github.com/Quingo/compiler_xtext/releases), and
2. the mlir-based compiler, which presents as a [binary executable](https://gitee.com/hpcl_quanta/quingo-runtime/releases).

The xtext compiler can generate eQASM instructions which can be simulated by PyQCAS and the mlir compiler can generate QCIS instructions which can be simulated by PyQCISim.

After downloading the binary, you need to call specify the compiler path for once in python using the following command:
```python
import quingo
# for xtext compiler
quingo.quingo_interface.set_xtext_compiler_path(<path-to-quingo.jar>)
# or for mlir compiler
quingo.quingo_interface.set_mlir_compiler_path(<path-to-quingoc>)
```

For the mlir compiler, you could also put it in a directory so that your terminal can find it, like `/usr/loca/bin/`. In this case, you no longer need to call `set_mlir_compiler_path` to specify its path.

### Special Care for Linux
Since the compiler executable `quingoc` depends on a number of libraries under linux, `quingoc` may not work well if you only download this executable binary. To cease the difficulty in running Quingo programs under linux, we have prepared a docker image (around 400MB) which prepares everything in ready. You can install it using the following command:
```sh
docker pull xsu1989/quingo:beta
docker run -it xsu1989/quingo:beta
cd examples && python3 host.py
```

In this case, you do not need to install anything else to run Quingo programs.

## Usage
A simple example can be found in the directory `src/examples`. You can simply run the bell_state example by running:
```sh
cd src/examples/bell_state
python host.py
```
If everything runs correctly, you should see the following output:
```sh
connecting pyqcisim_quantumsim...
num_qubits:  2
The result of bell_state is:
(['q0', 'q1'], {'00': 504, '01': 0, '10': 0, '11': 496})
```

## APIs of the Quingo runtime system


## Quingo programming tutorial
To be added.