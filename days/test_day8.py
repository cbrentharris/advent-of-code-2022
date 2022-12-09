import unittest
import os
import days
from days.day8 import part_1, part_2

example_data = ["30373", "25512", "65332", "33549", "35390"]
days_dir = os.path.dirname(days.__file__)
input_file_name = os.path.join(days_dir, "input_day8.txt")


class TestDay8(unittest.TestCase):
    def test_day8_part_1_example(self) -> None:
        self.assertEqual("21", part_1(example_data))

    def test_day8_part_1(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("1796", part_1(input_file.readlines()))

    def test_day8_part_2_example(self) -> None:
        self.assertEqual("8", part_2(example_data))

    def test_day8_part_2(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("288120", part_2(input_file.readlines()))


if __name__ == '__main__':
    unittest.main()
