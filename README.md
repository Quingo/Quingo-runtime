# Quingo Runtime System

Along with quingo compilers, the Quingo runtime system which provides users the capability to program and simulate Quingo programs.

## Installation


### Overview
The Quingo installation comprises of two main steps:

#### Runtime system and simulator
Install Quingo runtime system with required simulators using the following command:
```
pip install quingo
```

Upon success, it will automatically install the Quingo runtime system (this package), the PyQCAS simulator and the PyQCISim simulator.

#### The Quingo compiler
Since the Quingo runtime is a framework integrating and managing quantum and classical computational resources, it does not contain the quantum compiler by default. The Quingo compiler should be donwloaded separately.

Two versions of Quingo compiler has been developed:
1. the xtext-based compiler, which appears as a jar file, and
2. the mlir-based compiler, which presents as a binary [executable](https://gitee.com/hpcl_quanta/quingo-compiler).

For the xtext compiler, you should
put it in a directory so that your terminal can find it. Usually, we could put it in a directory in the path, like `/usr/loca/bin/`.


### Linux

###

## Usage
A simple example can be found in the directory `src/examples`. You can simply run the bell_state example by running:
```
cd src/examples/bell_state
python host.py
```
If everything runs correctly, you should see the following output:
```
connecting pyqcisim_quantumsim...
num_qubits:  2
The result of bell_state is:
(['q0', 'q1'], {'00': 504, '01': 0, '10': 0, '11': 496})
```

## APIs of the runtime system
To be added.

## Quingo programming tutorial
To be added.