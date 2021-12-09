# Quingo Runtime System

The Quingo runtime system.

**NOTE**:
- The code in the `master` branch is currently unstable.
- The more stable version can be found in the `develop` branch.

## Prerequisites
- Python 3.7
  - **NOTE**: Python **3.7** is required.
  - Python 3.6 **cannot** work.
  - Python 3.8 has not been tested.
- Java Development ToolKit (JDK)
  - you should install the latest version of [Java Development ToolKit](https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html). You may need to add or modify a few environmental  variables as well.
  - If you are using Ubuntu, you can install JDK8 with the following command: `sudo apt-get install openjdk-8-jdk`.
  - After a success installation, you should be able to execute this command: `java -version`.

## Installation
Enter the root directory of this project, and simply run either one of the two following commands:
```
python setup.py develop
```
or
```
pip install -e .
```




## Change Log
| Version |    Date    | Description                                              |
| :-----: | :--------: | -------------------------------------------------------- |
|  0.1.0  | 2021-12-08 | A big update, now supports mlir compiler and PyQCISim.   |
|  0.0.5  | 2020-07-14 | Updated Xtext compiler. Now supports default parameters. |

