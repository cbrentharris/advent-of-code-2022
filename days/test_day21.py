import unittest
import os
import days
from days.day21 import part_1, part_2

example_data = ["root: pppw + sjmn", "dbpl: 5", "cczh: sllz + lgvd", "zczc: 2", "ptdq: humn - dvpt", "dvpt: 3", "lfqf: 4", "humn: 5", "ljgn: 2", "sjmn: drzm * dbpl", "sllz: 4", "pppw: cczh / lfqf", "lgvd: ljgn * ptdq", "drzm: hmdt - zczc", "hmdt: 32"]
days_dir = os.path.dirname(days.__file__)
input_file_name = os.path.join(days_dir, "input_day21.txt")


class TestDay21(unittest.TestCase):
    def test_day21_part_1_example(self) -> None:
        self.assertEqual("152.0", part_1(example_data))

    def test_day21_part_1(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("", part_1(input_file.readlines()))

    def test_day21_part_2_example(self) -> None:
        self.assertEqual("", part_2(example_data))

    def test_day21_part_2(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("", part_2(input_file.readlines()))


if __name__ == '__main__':
    unittest.main()
