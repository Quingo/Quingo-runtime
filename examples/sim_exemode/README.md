## 使用
在本示例中展示了对于不同的模拟执行模式的输出
```sh
# 该示例展示了cfg = ExeConfig(ExeMode.SimFinalResult, num_shots)
# 的模拟结果输出
# ExeMode.SimFinalResult: Final Result.
# num_shots: number of simulation times.
python ./SimFinalResult.py
```
模拟结果如下：
```sh
sim res:  (['Q1', 'Q2'], [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [0, 0], [0, 0], [1, 1], [1, 1], [0, 0]])
```
针对StateVector的输出如下：
```sh
# 该示例展示了cfg = ExeConfig(ExeMode.SimStateVector)
# 的模拟结果输出
# ExeMode.SimStateVector: StateVector.
python ./SimStateVector.py
```
模拟结果如下：
```sh
sim res for bell state is:
classical: {}
quantum: (['Q1', 'Q2'], Matrix([
[sqrt(2)/2],
[        0],
[        0],
[sqrt(2)/2]]))
```