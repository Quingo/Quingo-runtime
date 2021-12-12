# Quingo Runtime System

Along with quingo compilers, the Quingo runtime system which provides users the capability to program and simulate Quingo programs.

## Installation
It comprises of two steps:

1. Install Quingo runtime system
```
pip install quingo
```

2. Download the quingo compiler executable from [this site](https://gitee.com/hpcl_quanta/quingo-compiler) and put it in a directory so that your terminal can find it. Usually, we could put it in a directory in the path, like `/usr/loca/bin/`.


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