import pytest
import numpy as np
from pathlib import Path
import tempfile
import os
import sys
import importlib.util
from quingo.cim.parser import read_coupling_graph, read_plain_matrix, read_J

# 直接从文件路径导入parser模块
# parser_path = Path(__file__).parent.parent / "src" / "quingo" / "cim" / "parser.py"
# spec = importlib.util.spec_from_file_location("parser", parser_path)
# parser_module = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(parser_module)

# 从模块中获取函数
# read_coupling_graph = parser_module.read_coupling_graph
# read_plain_matrix = parser_module.read_plain_matrix
# read_J = parser_module.read_J


class TestParser:
    """parser.py 模块的单元测试"""

    @classmethod
    def setup_class(cls):
        """设置测试类，定义测试数据文件路径"""
        cls.test_data_dir = Path(__file__).parent / "test_data"
        cls.plain_matrix_file = cls.test_data_dir / "plain_matrix.txt"
        cls.small_matrix_file = cls.test_data_dir / "small_matrix.txt"
        cls.coupling_graph_file = cls.test_data_dir / "coupling_graph.txt"
        cls.invalid_matrix_file = cls.test_data_dir / "invalid_matrix.txt"
        cls.nonexistent_file = cls.test_data_dir / "nonexistent.txt"

    def test_read_plain_matrix_success(self):
        """测试 read_plain_matrix 函数正常读取"""
        # 测试读取5x5矩阵
        matrix = read_plain_matrix(self.plain_matrix_file)
        expected_matrix = np.array([
            [0, 1, 0, 0, 0],
            [1, 0, 1, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 1, 0, 1],
            [0, 0, 0, 1, 0]
        ], dtype=float)

        assert matrix.shape == (5, 5)
        np.testing.assert_array_equal(matrix, expected_matrix)

    def test_read_plain_matrix_small(self):
        """测试 read_plain_matrix 函数读取小矩阵"""
        matrix = read_plain_matrix(self.small_matrix_file)
        expected_matrix = np.array([
            [1.0, 2.0],
            [3.0, 4.0]
        ], dtype=float)

        assert matrix.shape == (2, 2)
        np.testing.assert_array_equal(matrix, expected_matrix)

    def test_read_plain_matrix_string_path(self):
        """测试 read_plain_matrix 函数接受字符串路径参数"""
        matrix = read_plain_matrix(str(self.small_matrix_file))
        expected_matrix = np.array([
            [1.0, 2.0],
            [3.0, 4.0]
        ], dtype=float)

        assert matrix.shape == (2, 2)
        np.testing.assert_array_equal(matrix, expected_matrix)

    def test_read_plain_matrix_file_not_found(self):
        """测试 read_plain_matrix 函数文件不存在异常"""
        with pytest.raises(FileNotFoundError) as exc_info:
            read_plain_matrix(self.nonexistent_file)

        assert "文件未找到" in str(exc_info.value)
        assert str(self.nonexistent_file) in str(exc_info.value)

    def test_read_plain_matrix_invalid_format(self):
        """测试 read_plain_matrix 函数文件格式错误异常"""
        with pytest.raises(ValueError):
            read_plain_matrix(self.invalid_matrix_file)

    def test_read_coupling_graph_success(self):
        """测试 read_coupling_graph 函数正常读取"""
        expected_matrix = np.array([
            [0, 1, 0, 0, 0],
            [1, 0, 1, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 1, 0, 1],
            [0, 0, 0, 1, 0]
        ], dtype=float)

        matrix = read_coupling_graph(self.coupling_graph_file)

        assert matrix.shape == (5, 5)
        np.testing.assert_array_equal(matrix, expected_matrix)

    def test_read_coupling_graph_string_path(self):
        """测试 read_coupling_graph 函数接受字符串路径参数"""
        expected_matrix = np.array([
            [0, 1, 0, 0, 0],
            [1, 0, 1, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 1, 0, 1],
            [0, 0, 0, 1, 0]
        ], dtype=float)

        matrix = read_coupling_graph(str(self.coupling_graph_file))

        assert matrix.shape == (5, 5)
        np.testing.assert_array_equal(matrix, expected_matrix)

    def test_read_coupling_graph_file_not_found(self):
        """测试 read_coupling_graph 函数文件不存在异常"""
        with pytest.raises(FileNotFoundError) as exc_info:
            read_coupling_graph(self.nonexistent_file)

        assert "文件未找到" in str(exc_info.value)
        assert str(self.nonexistent_file) in str(exc_info.value)

    def test_read_coupling_graph_value_error(self):
        """测试 read_coupling_graph 函数文件格式错误异常"""
        # 创建一个格式错误的耦合图文件
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write("invalid format\ndata")
            temp_file_path = temp_file.name

        try:
            with pytest.raises(ValueError) as exc_info:
                read_coupling_graph(temp_file_path)

            assert "文件内容格式错误" in str(exc_info.value)
        finally:
            os.unlink(temp_file_path)

    def test_read_plain_matrix_with_empty_file(self):
        """测试 read_plain_matrix 函数读取空文件"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write("")
            temp_file_path = temp_file.name

        try:
            matrix = read_plain_matrix(temp_file_path)
            # 空文件应该返回空数组
            assert matrix.size == 0
        except ValueError:
            # 空文件可能抛出 ValueError，这也是可接受的行为
            pass
        finally:
            os.unlink(temp_file_path)

    def test_read_plain_matrix_with_whitespace_only(self):
        """测试 read_plain_matrix 函数读取只有空白字符的文件"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write("   \n\n  \t\n")
            temp_file_path = temp_file.name

        try:
            matrix = read_plain_matrix(temp_file_path)
            # 只有空白字符的文件应该返回空数组或抛出异常
            assert matrix.size == 0
        except ValueError:
            # 这是可接受的行为
            pass
        finally:
            os.unlink(temp_file_path)

    def test_read_plain_matrix_mixed_data_types(self):
        """测试 read_plain_matrix 函数读取包含不同数据类型的文件"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write("1.0 2\n3.5 4.0")
            temp_file_path = temp_file.name

        try:
            matrix = read_plain_matrix(temp_file_path)
            expected_matrix = np.array([
                [1.0, 2.0],
                [3.5, 4.0]
            ], dtype=float)

            assert matrix.shape == (2, 2)
            np.testing.assert_array_equal(matrix, expected_matrix)
        finally:
            os.unlink(temp_file_path)

    # read_J 函数的直接测试
    def test_read_J_success(self):
        """测试 read_J 函数正常读取"""
        expected_matrix = np.array([
            [0, 1, 0, 0, 0],
            [1, 0, 1, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 1, 0, 1],
            [0, 0, 0, 1, 0]
        ], dtype=float)

        matrix = read_J(self.coupling_graph_file)

        assert matrix.shape == (5, 5)
        np.testing.assert_array_equal(matrix, expected_matrix)

    def test_read_J_string_path(self):
        """测试 read_J 函数接受字符串路径参数"""
        expected_matrix = np.array([
            [0, 1, 0, 0, 0],
            [1, 0, 1, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 1, 0, 1],
            [0, 0, 0, 1, 0]
        ], dtype=float)

        matrix = read_J(str(self.coupling_graph_file))

        assert matrix.shape == (5, 5)
        np.testing.assert_array_equal(matrix, expected_matrix)

    def test_read_J_empty_file(self):
        """测试 read_J 函数读取空文件"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write("")
            temp_file_path = temp_file.name

        try:
            with pytest.raises(ValueError) as exc_info:
                read_J(temp_file_path)

            assert "文件内容为空" in str(exc_info.value)
        finally:
            os.unlink(temp_file_path)

    def test_read_J_single_line_file(self):
        """测试 read_J 函数读取只有一行的文件"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write("5 4")
            temp_file_path = temp_file.name

        try:
            with pytest.raises(ValueError) as exc_info:
                read_J(temp_file_path)

            assert "文件内容格式错误" in str(exc_info.value)
        finally:
            os.unlink(temp_file_path)

    def test_read_J_invalid_header(self):
        """测试 read_J 函数读取头部格式错误的文件"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write("invalid header\n1 2 1.0")
            temp_file_path = temp_file.name

        try:
            with pytest.raises(ValueError) as exc_info:
                read_J(temp_file_path)

            assert "invalid literal for int() with base 10:" in str(exc_info.value)
        finally:
            os.unlink(temp_file_path)

    def test_read_J_edge_count_mismatch(self):
        """测试 read_J 函数边数不匹配"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write("3 2\n1 2 1.0")  # 声明2条边但只有1条
            temp_file_path = temp_file.name

        try:
            with pytest.raises(ValueError) as exc_info:
                read_J(temp_file_path)

            assert "文件内容格式错误" in str(exc_info.value)
        finally:
            os.unlink(temp_file_path)

    def test_read_J_invalid_edge_format(self):
        """测试 read_J 函数边格式错误"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
            temp_file.write("3 2\n1 2\n2 3 1.0")  # 第一条边缺少权重
            temp_file_path = temp_file.name

        try:
            with pytest.raises(ValueError) as exc_info:
                read_J(temp_file_path)

            assert "文件内容格式错误" in str(exc_info.value)
        finally:
            os.unlink(temp_file_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])