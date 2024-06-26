from quingo.backend.pyqcisim_tequila import PyQCISim_tequila
from quingo.backend.pyqcisim_quantumsim import PyQCISim_quantumsim
from quingo.backend.qualesim import QuaLeSim
from quingo.backend.symqc import IfSymQC
from quingo.backend.backend_hub import BackendType, Backend_hub
from quingo.backend.qisa import Qisa
from quingo.core.exe_config import *
import threading
from quingo.utils import number_distance
from pathlib import Path


unittest_dir = Path(__file__).parent / ".."
qcis_fn = unittest_dir / "test_qcis" / "bell.qcis"
qcis_fn2 = unittest_dir / "test_qcis" / "bell_no_msmt.qcis"
quiet_fn = unittest_dir / "test_qcis" / "bell.qi"
quiet_fn2 = unittest_dir / "test_qcis" / "bell_no_msmt.qi"


# progress: 2023-10-09
# finished test on quantumsim and Tequila.
class Test_backends:
    def test_basic(self):
        def single(BackendClass, type, qisa, is_sim):
            sim = BackendClass()
            assert sim.get_type() == type
            assert sim.get_qisa() == qisa
            assert sim.is_simulator() == is_sim

        # QuaLeSim_tequila and QuaLeSim_quantumsim default Qisa type is QCIS
        # single(QuaLeSim_tequila, BackendType.QUALESIM_TEQUILA, Qisa.QCIS, True)
        single(QuaLeSim, BackendType.QUALESIM_QUANTUMSIM, Qisa.QCIS, True)
        single(PyQCISim_tequila, BackendType.TEQUILA, Qisa.QCIS, True)
        single(PyQCISim_quantumsim, BackendType.QUANTUM_SIM, Qisa.QCIS, True)
        single(IfSymQC, BackendType.SYMQC, Qisa.QCIS, True)

    def test_upload_program(self):
        def single(BackendClass, qasm_fn):
            sim = BackendClass()
            try:
                sim.upload_program(qasm_fn)
            except Exception as e:
                assert False, "upload_program failed: {}".format(e)

        # single(QuaLeSim_tequila, qcis_fn)
        # single(QuaLeSim_tequila, quiet_fn)
        single(QuaLeSim, qcis_fn)
        single(QuaLeSim, quiet_fn)
        single(PyQCISim_tequila, qcis_fn)
        single(PyQCISim_quantumsim, qcis_fn)
        single(IfSymQC, qcis_fn)

    def test_get_from_hub(self):
        def single(backend_type, simulator_class):
            hub = Backend_hub()
            sim = hub.get_instance(backend_type)
            assert isinstance(sim, simulator_class)

        single(BackendType.QUANTUM_SIM, PyQCISim_quantumsim)
        single(BackendType.TEQUILA, PyQCISim_tequila)
        single(BackendType.QUALESIM_QUANTUMSIM, QuaLeSim)
        single(BackendType.SYMQC, IfSymQC)


if __name__ == "__main__":
    pass
