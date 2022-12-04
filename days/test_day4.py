import unittest
import os
import days
from days.day4 import part_1, part_2

example_data = ["2-4,6-8", "2-3,4-5", "5-7,7-9", "2-8,3-7", "6-6,4-6", "2-6,4-8"]
days_dir = os.path.dirname(days.__file__)
input_file_name = os.path.join(days_dir, "input_day4.txt")


class TestDay4(unittest.TestCase):
    def test_day4_part_1_example(self) -> None:
        self.assertEqual("2", part_1(example_data))

    def test_day4_part_1(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("576", part_1(input_file.readlines()))

    def test_day4_part_2_example(self) -> None:
        self.assertEqual("4", part_2(example_data))

    def test_day4_part_2(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("905", part_2(input_file.readlines()))


if __name__ == '__main__':
    unittest.main()
