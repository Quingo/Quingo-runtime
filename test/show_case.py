from pathlib import Path
from quingo import Quingo_interface

qi = Quingo_interface()

prj_root = Path(__file__).absolute().parent.parent
bell_fn = prj_root / "examples" / "ghz" / "kernel.qu"


qasm_fn = qi.compile(bell_fn, "ghz", 3)
