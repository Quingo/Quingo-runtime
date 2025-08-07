# Quingo Backend Result Format
Currently, Quingo supports four kinds of result format:
- SimShots (shot)
- SimFinalResult (final result)
- SimStateVector (state vector)
- SymbolicStateVector (symbolic state vector)

The real machine can only return the result in the shot mode.

## SimShot
In this mode, only classical information will be recorded, and the quantum state will be dropped. An extra parameter `num_shots` is accepted for this mode, which tells how many times this experiment will be repeated for.

The output is a 2-element tuple:
    - a list of qubit names or classical variables (`names`)
    - a 2-d list, with i-th value in the j-th inner list corresponding to the i-th qubit or classical variable in `names` in the j-th run.

An Example result of a simulation with num_shots=3:
```python
(['Q3', 'Q4', 'Q5', 'Q6', 'Q7'],
 [[1, 1, 0, 0, 0],
  [1, 1, 0, 0, 0],
  [1, 1, 0, 0, 0]])
```

## SimStateVector
In this mode, measurements are only allowed at the end of the entire program, and no mid-circuit measurement is allowed. All measurements in the end will be dropped while performing the simulation.

result is a tuple that contains two elements:
- The first element is a list of qubits, and
- the second element is a complex array representing the state of the quantum system (which is a 1-d list).

Example:
For the following QUIET-s program:
```quiet
func main()->(int c1, int c2):
    qubit q1
    qubit q2
    H q1
    CNOT q1, q2
end
```

The result shall be:
```python
 (
    ['q1', 'q2'],
    [(0.7071067811865474+0j), 0j, 0j, (0.7071067811865476+0j)]
 )
```

## SymbolicStateVector
Everything is the same as `SimStateVector`, except that the state is represented using symbols in sympy.

## SimFinalResult
In this mode, both classical result and quantum result will be returned in a dictionary. The `num_shots` parameter is not allowed in this mode.

- The `classical` result is a dictionary that maps classical variables to their values. Each key-value pair represents a classical variable and its corresponding value.

- The `quantum` result is a tuple that contains two elements. The first element is a list of qubits, and the second element is a complex array representing the state of the quantum system. The qubits are represented as strings in the list. The complex array represents the amplitudes of the quantum states, where each element corresponds to a specific quantum state.

For example:
```quiet
func main()->(int c1, int c2):
    qubit q1
    qubit q2
    H q1
    CNOT q1, q2
    measure(q1)->c1
end
```

Two runs of this program returns different results:
```python
 {'classical': {'q1': 1}, 'quantum': (['q2'], [0j, (1+0j)])}
```

```python
{'classical': {'q1': 0}, 'quantum': (['q2'], [(1+0j), 0j])}
```
