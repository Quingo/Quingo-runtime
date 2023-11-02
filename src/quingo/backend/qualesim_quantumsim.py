# from .backend_hub import BackendType
# from .if_backend import If_backend
# from quingo.core.exe_config import *
# from quingo.core.utils import *
# from dqcsim.plugin import *
# from dqcsim.host import *

# logger = get_logger((__name__).split(".")[-1])


# class QuaLeSim_quantumsim(If_backend):
#     """A functional QCIS simulation backend using PyQCISim and Tequila."""

#     def __init__(self):
#         super().__init__(BackendType.QUALESIM_QUANTUMSIM)
#         self.sim = Simulator(stderr_verbosity=Loglevel.OFF)
#         self.sim.with_backend("quantumsim", verbosity=Loglevel.OFF)
#         self.res = None

#     def upload_program(self, prog_fn):
#         prog_fn = ensure_path(prog_fn)
#         if str(prog_fn).endswith(".qcis") or str(prog_fn).endswith(".qi"):
#             self.sim.with_frontend(str(prog_fn), verbosity=Loglevel.OFF)
#         else:
#             raise TypeError(
#                 "The quantumsim simulator can only accept QCIS or QUIET-S instructions."
#             )

#     def execute(self, exe_config: ExeConfig):
#         if exe_config.mode == ExeMode.SimFinalResult:
#             measure_mod = "one_shot"
#             try:
#                 self.sim.simulate()
#                 res = self.sim.run(
#                     measure_mod=measure_mod, num_shots=exe_config.num_shots
#                 )
#                 self.sim.stop()
#                 final_state = res["res"]
#                 final_state["quantum"] = tuple(final_state["quantum"])
#                 return final_state["quantum"]
#             except:
#                 raise ValueError(
#                     "Here is some wrong with ({}) for QUALESIM_QUANTUMSIM.".format(
#                         exe_config.mode
#                     )
#                 )

#         if exe_config.mode == ExeMode.SimStateVector:
#             measure_mod = "state_vector"
#             try:
#                 self.sim.simulate()
#                 res = self.sim.run(measure_mod=measure_mod)
#                 self.sim.stop()
#                 final_state = eval(res["res"])
#                 return final_state
#             except:
#                 raise ValueError(
#                     "Here is some wrong with ({}) for QUALESIM_QUANTUMSIM.".format(
#                         exe_config.mode
#                     )
#                 )

#         raise ValueError(
#             "Here is some wrong with ({}) for QUALESIM_QUANTUMSIM.".format(
#                 exe_config.mode
#             )
#         )
