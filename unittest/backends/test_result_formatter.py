import unittest
from quingo.backend.result_formatter import get_first_non_zero_res, reorder_bits


class TestResultFormatter(unittest.TestCase):
    def test_no_measure_results(self):
        with self.assertRaises(ValueError):
            get_first_non_zero_res(None)

    def test_no_measure_results_found(self):
        shots_result = (["Q3", "Q4", "Q5", "Q6", "Q7"], None)
        with self.assertRaises(ValueError):
            get_first_non_zero_res(shots_result)

    def test_integer_format_little_endian(self):
        shots_result = (
            ["Q3", "Q4", "Q5", "Q6", "Q7"],
            [[1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 1, 0, 0, 0]],
        )
        result = get_first_non_zero_res(shots_result)
        self.assertEqual(result, 0b00011)

    def test_integer_format_big_endian(self):
        shots_result = (
            ["Q3", "Q4", "Q5", "Q6", "Q7"],
            [[1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 1, 0, 0, 0]],
        )
        result = get_first_non_zero_res(shots_result, little_endian=False)
        self.assertEqual(result, 0b11000)

    def test_list_format_little_endian(self):
        shots_result = (
            ["Q3", "Q4", "Q5", "Q6", "Q7"],
            [[1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 1, 0, 0, 0]],
        )
        result = get_first_non_zero_res(shots_result, integer_format=False)
        self.assertEqual(result, [0, 0, 0, 1, 1])

    def test_list_format_big_endian(self):
        shots_result = (
            ["Q3", "Q4", "Q5", "Q6", "Q7"],
            [[1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 1, 0, 0, 0]],
        )
        result = get_first_non_zero_res(
            shots_result, integer_format=False, little_endian=False
        )
        self.assertEqual(result, [1, 1, 0, 0, 0])

    def test_specific_qubits(self):
        shots_result = (
            ["Q3", "Q4", "Q5", "Q6", "Q7"],
            [[1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [1, 1, 0, 0, 0]],
        )
        result = get_first_non_zero_res(shots_result, qubits=["Q4", "Q5"])
        self.assertEqual(result, 0b01)

    def test_reorder_bits_ascending(self):
        qubit_list = ["Q3", "Q1", "Q4", "Q2"]
        qubit_msmt_res = [1, 1, 0, 0]
        expected_result = [1, 0, 1, 0]
        result = reorder_bits(qubit_list, qubit_msmt_res)
        self.assertEqual(result, expected_result)

    def test_reorder_bits_descending(self):
        qubit_list = ["Q3", "Q1", "Q4", "Q2"]
        qubit_msmt_res = [1, 1, 0, 0]
        expected_result = [0, 1, 0, 1]
        result = reorder_bits(qubit_list, qubit_msmt_res, Ascending=False)
        self.assertEqual(result, expected_result)

    def test_reorder_bits_same_order(self):
        qubit_list = ["Q1", "Q2", "Q3", "Q4"]
        qubit_msmt_res = [1, 0, 1, 0]
        expected_result = [1, 0, 1, 0]
        self.assertEqual(
            reorder_bits(qubit_list, qubit_msmt_res, Ascending=True), expected_result
        )

    def test_reorder_bits_empty_input(self):
        qubit_list = []
        qubit_msmt_res = []
        expected_result = []
        self.assertEqual(
            reorder_bits(qubit_list, qubit_msmt_res, Ascending=True), expected_result
        )

    def test_reorder_bits_more_qubits(self):
        qubit_list = ["Q6", "Q3", "Q1", "Q4", "Q2", "Q5"]
        qubit_msmt_res = [1, 1, 0, 0, 1, 0]
        expected_result = [0, 1, 1, 0, 0, 1]
        self.assertEqual(
            reorder_bits(qubit_list, qubit_msmt_res, Ascending=True), expected_result
        )

    def test_reorder_bits_fewer_qubits(self):
        qubit_list = ["Q2", "Q1"]
        qubit_msmt_res = [1, 0]
        expected_result = [0, 1]
        self.assertEqual(
            reorder_bits(qubit_list, qubit_msmt_res, Ascending=True), expected_result
        )


if __name__ == "__main__":
    unittest.main()
