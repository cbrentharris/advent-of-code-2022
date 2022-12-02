import unittest
import os
import days
from days.day2 import part_1, part_2

example_data = ["A Y", "B X", "C Z"]
days_dir = os.path.dirname(days.__file__)
input_file_name = os.path.join(days_dir, "input_day2.txt")


class TestDay2(unittest.TestCase):
    def test_day2_part_1_example(self) -> None:
        self.assertEqual("15", part_1(example_data))

    def test_day2_part_1(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("11841", part_1(input_file.readlines()))

    def test_day2_part_2_example(self) -> None:
        self.assertEqual("12", part_2(example_data))

    def test_day2_part_2(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("13022", part_2(input_file.readlines()))


if __name__ == '__main__':
    unittest.main()
