import pytest
from quingo.core.preparation import *
from pathlib import Path

unittest_dir = Path(__file__).parent
qu_dir = unittest_dir / "test_qu"


class TestPrepareMain:
    def test_get_type(self):
        def single_test(src, func_name, expected_type):
            assert get_ret_type(src, func_name) == expected_type

        single_test("""operation foo(): unit {}""", "foo", "unit")
        single_test("""operation foo(): {}""", "foo", "unit")
        single_test(
            """
            operation foo(): int {
                return 1;
            }
            """,
            "foo",
            "int",
        )
        single_test(
            """
            operation foo(): bool {
                return 1;
            }
            """,
            "foo",
            "bool",
        )
        single_test(
            """
            operation foo(): (bool, int) {
                return 1;
            }
            """,
            "foo",
            "(bool, int)",
        )
        with pytest.raises(ValueError):
            single_test(
                """
                operation foo(): (bool, int) {
                    return 1;
                }
                """,
                "bar",
                "(bool, int)",
            )

    def test_gen_main_func(self):
        mock_fn = """
operation foo(a: int, b: int): int {
    return 1;
}"""
        main_func = gen_main_func(mock_fn, "foo", (1, 2))
        lines = main_func.split("\n")
        # remove empty lines
        lines = [line.strip() for line in lines if line.strip() != ""]
        assert lines[0].startswith("operation main() : int")
        assert lines[1].startswith("int var0_int;")
        assert lines[2].startswith("var0_int = 1;")
        assert lines[3].startswith("int var1_int;")
        assert lines[4].startswith("var1_int = 2;")
        assert lines[5].startswith("return foo(var0_int, var1_int);")

    def test_gen_main_file(self):
        mock_file = qu_dir / "mock.qu"
        mock_main_fn = qu_dir / "mock_main.qu"
        mock_main_fn.unlink(missing_ok=True)

        gen_main_file(mock_file, "foo", mock_main_fn, (1, 2))
        assert mock_main_fn.exists()

        with mock_main_fn.open() as f:
            lines = f.readlines()
        # remove empty lines
        lines = [line for line in lines if line.strip() != ""]
        lines[0].startswith("import")
        lines[1].startswith("operation main() : int")

    def test_gen_main_func_with_single_qubit_alloc(self):
        """When `qubit_alloc=["cq30"]` is given, the generated main must:
        1. wrap the entry call in `using (cq30: qubit) { ... }`;
        2. prepend `cq30` as the first positional argument of the call.
        """
        mock_fn = """
operation t1_experiment(q: qubit, t1_delay: time): unit {
    wait(q, t1_delay);
}"""
        main_func = gen_main_func(
            mock_fn, "t1_experiment", (1.0,), qubit_alloc=["cq30"]
        )
        non_empty = [ln.strip() for ln in main_func.split("\n") if ln.strip()]
        assert non_empty[0].startswith("operation main() : unit")
        assert "double var0_double;" in non_empty
        assert "var0_double = 1.0;" in non_empty
        using_lines = [ln for ln in non_empty if ln.startswith("using")]
        assert len(using_lines) == 1
        assert using_lines[0] == "using (cq30: qubit) {"
        call_lines = [ln for ln in non_empty if "t1_experiment(" in ln]
        assert call_lines == ["t1_experiment(cq30, var0_double);"]

    def test_gen_main_func_with_multi_qubit_alloc(self):
        """Multiple qubits should appear in declaration & call order."""
        mock_fn = """
operation cz_pair(qa: qubit, qb: qubit): unit { CZ(qa, qb); }"""
        main_func = gen_main_func(mock_fn, "cz_pair", (), qubit_alloc=["cq30", "cq31"])
        non_empty = [ln.strip() for ln in main_func.split("\n") if ln.strip()]
        assert "using (cq30: qubit, cq31: qubit) {" in non_empty
        assert "cz_pair(cq30, cq31);" in non_empty

    def test_gen_main_func_qubit_alloc_none_is_legacy(self):
        """qubit_alloc=None must reproduce the exact legacy behaviour."""
        mock_fn = """
operation foo(a: int): int { return a; }"""
        legacy = gen_main_func(mock_fn, "foo", (5,))
        with_none = gen_main_func(mock_fn, "foo", (5,), qubit_alloc=None)
        with_empty = gen_main_func(mock_fn, "foo", (5,), qubit_alloc=[])
        assert legacy == with_none == with_empty


if __name__ == "__main__":
    TestPrepareMain().test_get_type()
    TestPrepareMain().test_gen_main_func()
    TestPrepareMain().test_gen_main_file()
    TestPrepareMain().test_gen_main_func_with_single_qubit_alloc()
    TestPrepareMain().test_gen_main_func_with_multi_qubit_alloc()
    TestPrepareMain().test_gen_main_func_qubit_alloc_none_is_legacy()
