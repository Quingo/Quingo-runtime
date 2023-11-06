import pytest
from quingo.core.preparation import *
from pathlib import Path
from global_config import SRC_PATH

cur_dir = SRC_PATH / "unittest" / ""
qu_dir = cur_dir / "test_qu" / ""


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


if __name__ == "__main__":
    TestPrepareMain().test_get_type()
    TestPrepareMain().test_gen_main_func()
    TestPrepareMain().test_gen_main_file()
