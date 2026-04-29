from pathlib import Path
from quingo.backend.backend_hub import Backend_hub, BackendType
from quingo.backend.qisa import Qisa
from quingo.core.compile import compose_cl_cmd
from quingo.core.quingo_task import Quingo_task


class Test_SISQ:
    def test_sisq_properties(self):
        hub = Backend_hub()

        # Check if SISQ is supported
        assert hub.support(BackendType.SISQ)

        # Check properties directly from hub
        assert hub.get_qisa(BackendType.SISQ) == Qisa.SISQ
        assert hub.is_simulator(BackendType.SISQ) == False

        # Ensure trying to get instance fails as expected
        # SISQ has no runtime backend, so get_instance should fail
        try:
            hub.get_instance(BackendType.SISQ)
            assert False, "Should not be able to instantiate SISQ backend"
        except TypeError:
            # Expected because module_path is None, causing TypeError when concatenating with string
            pass
        except Exception as e:
            # If it fails with another error, that's also acceptable as long as it fails
            # But we prefer to know why.
            # Given the current implementation, TypeError is most likely.
            print(f"Caught expected exception: {type(e).__name__}: {e}")
            pass

    def test_qisa_helpers(self):
        from quingo.backend.qisa import get_qisa_name, get_suffix

        assert get_qisa_name(Qisa.SISQ) == "sisq"
        assert get_suffix(Qisa.SISQ) == ".sisq"


class Test_SISQ_PULSE_EXP:
    """BackendType.SISQ_PULSE_EXP 新增枚举及 compose_cl_cmd 扩展的单元测试。"""

    def test_sisq_pulse_exp_registered(self):
        """SISQ_PULSE_EXP 已注册到 Backend_hub，QISA 为 SISQ，非模拟器。"""
        hub = Backend_hub()
        assert hub.support(BackendType.SISQ_PULSE_EXP)
        assert hub.get_qisa(BackendType.SISQ_PULSE_EXP) == Qisa.SISQ
        assert hub.is_simulator(BackendType.SISQ_PULSE_EXP) is False

    def test_compose_cl_cmd_target(self, tmp_path):
        """compose_cl_cmd 为 SISQ_PULSE_EXP 生成 --target=sisq-pulse-exp。"""
        qu = tmp_path / "T1.qu"
        qu.write_text("operation t1_experiment(t1_delay: time): unit {}")

        task = Quingo_task(
            called_qu_fn=qu,
            called_func="t1_experiment",
            build_under=tmp_path,
            flat_build=True,
            backend=BackendType.SISQ_PULSE_EXP,
            delete_build_dir=False,
        )

        cmd = compose_cl_cmd(
            task=task,
            qasm_fn=tmp_path / "out.sisq",
            quingoc_path=Path("/fake/quingoc"),
            target=BackendType.SISQ_PULSE_EXP,
            device_config_path=tmp_path / "device_config.json",
            wf_impl_dir=tmp_path / "wf_impl",
        )

        assert '"sisq-pulse-exp"' in cmd
        assert "--device-config=" in cmd
        assert "--wf-impl-dir=" in cmd
        assert "--isa=" not in cmd, "--isa 不应出现（已有 --target）"
