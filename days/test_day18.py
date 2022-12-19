import unittest
import os
import days
from days.day18 import part_1, part_2

example_data = ["2,2,2", "1,2,2", "3,2,2", "2,1,2", "2,3,2", "2,2,1", "2,2,3", "2,2,4", "2,2,6", "1,2,5", "3,2,5", "2,1,5", "2,3,5"]
days_dir = os.path.dirname(days.__file__)
input_file_name = os.path.join(days_dir, "input_day18.txt")


class TestDay18(unittest.TestCase):
    def test_day18_part_1_example(self) -> None:
        self.assertEqual("64", part_1(example_data))

    def test_day18_part_1(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("3396", part_1(input_file.readlines()))

    def test_day18_part_2_example(self) -> None:
        self.assertEqual("", part_2(example_data))

    def test_day18_part_2(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("", part_2(input_file.readlines()))


if __name__ == '__main__':
    unittest.main()
