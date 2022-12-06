import unittest
import os
import days
from days.day6 import part_1, part_2

example_data = ["mjqjpqmgbljsphdztnvjfqwrcgsmlb"]
days_dir = os.path.dirname(days.__file__)
input_file_name = os.path.join(days_dir, "input_day6.txt")


class TestDay6(unittest.TestCase):
    def test_day6_part_1_example(self) -> None:
        self.assertEqual("7", part_1(example_data))

    def test_day6_part_1(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("1757", part_1(input_file.readlines()))

    def test_day6_part_2_example(self) -> None:
        self.assertEqual("19", part_2(example_data))

    def test_day6_part_2(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("2950", part_2(input_file.readlines()))


if __name__ == '__main__':
    unittest.main()
