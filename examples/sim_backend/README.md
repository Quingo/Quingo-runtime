## 使用
在本示例中展示了调用不同的模拟后端的区别
```sh
# 在execute部分可以选取不同的backend来进行模拟，目前可供选择的后端有
# TEUQILA、QUANTUM_SIM和SYMQC
# res = execute(qasm_fn, BackendType.SYMQC, cfg)
python ./SimFinalResult.py
```
模拟结果如下：
```sh
sim res:  (['Q1', 'Q2'], [[0, 0], [0, 0], [1, 1], [1, 1], [1, 1], [0, 0], [1, 1], [1, 1], [1, 1], [0, 0]])
```
