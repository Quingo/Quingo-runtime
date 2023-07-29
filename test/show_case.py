from pathlib import Path
from quingo import Quingo_interface, Quingo_task

qi = Quingo_interface()

prj_root = Path(__file__).absolute().parent.parent
bell_fn = prj_root / "examples" / "ghz" / "kernel.qu"

# method 1: compile and execute the program separately
task = Quingo_task(bell_fn, "ghz")
qasm_fn = qi.compile(task, params=(3,), qasm_fn="ghz.qasm")
qasm_fn = qi.compile(task, params=(3,))
backend = "tequila"
res = qi.execute(qasm_fn, backend)


# method 2: compile and execute the program in one step
task = Quingo_task(bell_fn, "ghz", "tequila")
# this function supports passing parameters to Quingo and  generate
# a Quingo `main` function for the given task
res = qi.call(task, 3)

# method 3: invoke an independent quingo file
task = Quingo_task(bell_fn, "tequila")
# this function calls the backend to execute the given Quingo task
# no parameter will be passed and no `main` function will be generated
res = qi.invoke(task)
