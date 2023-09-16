## the result
1. 对于state_vector模式
    - 结果如下：
    ```
    模拟：
    .file:
    .gate:
    .body:
        func main()->(int c1, int c2):
            qubit q1
            qubit q2
            H q1
            CNOT q1, q2
        end
    res = {'classical': {}, 'quantum': (['q1', 'q2'], [(0.7071067811865474+0j), 0j, 0j, (0.7071067811865476+0j)])}

    模拟：
    .file:
    .gate:
    .body:
        func main()->(int c1, int c2):
            qubit q1
            qubit q2
            H q1
            CNOT q1, q2
            measure(q1)->c1
        end
    res = {'classical': {'q1': 1}, 'quantum': (['q2'], [0j, (1+0j)])}
    //
    res = {'classical': {'q1': 0}, 'quantum': (['q2'], [(1+0j), 0j])}
    ```
    - 对于未测量的量子比特，返回量子比特序列及其对应的状态向量
    - 对于已测量的量子比特，将其及对应的测量值存入classical中，quantum中存储未测量的量子比特的状态向量。（暂时未考虑重复利用已测量的量子比特的情况……）