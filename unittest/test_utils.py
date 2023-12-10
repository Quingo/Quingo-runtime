import quingo.backend.result_formatter as rf


class Test_result_formater:
    def test_reorder_bits(self):
        def single_test_case(qubit_list, str_bit_list, expected):
            res = rf.reorder_bits(qubit_list, str_bit_list)
            print(res)
            assert res == expected

        qubit_list = ["Q1", "Q2", "Q3", "Q4"]
        single_test_case(qubit_list, "0001", "0001")
        single_test_case(qubit_list, "0010", "0010")
        single_test_case(qubit_list, "0100", "0100")
        single_test_case(qubit_list, "1000", "1000")
        qubit_list = ["Q2", "Q1", "Q4", "Q3"]
        single_test_case(qubit_list, "0001", "0010")
        single_test_case(qubit_list, "0010", "0001")
        single_test_case(qubit_list, "0100", "1000")
        single_test_case(qubit_list, "1000", "0100")
        qubit_list = ["Q2", "Q4", "Q3", "Q1"]
        single_test_case(qubit_list, "1001", "1100")
        single_test_case(qubit_list, "0001", "1000")
        single_test_case(qubit_list, "0110", "0011")
        single_test_case(qubit_list, "0100", "0001")

        qubit_list = ["Q3", "Q4", "Q5", "Q6", "Q7"]
        single_test_case(qubit_list, "00011", "00011")
        single_test_case(qubit_list, "01100", "01100")
        single_test_case(qubit_list, "11000", "11000")

        qubit_list = ["Q6", "Q8", "Q2", "Q4", "Q9"]
        single_test_case(qubit_list, "00011", "01001")
        single_test_case(qubit_list, "01100", "10010")
        single_test_case(qubit_list, "11000", "00110")


if __name__ == "__main__":
    test = Test_result_formater()
    test.test_reorder_bits()
