import unittest
import os
import days
from days.day1 import part_1, part_2

example_data = ["1000", "2000", "3000", "", "4000", "", "5000", "6000", "", "7000", "8000", "9000", "", "10000"]
days_dir = os.path.dirname(days.__file__)
input_file_name = os.path.join(days_dir, "input_day1.txt")


class TestDay1(unittest.TestCase):
    def test_day1_part_1_example(self) -> None:
        self.assertEqual("24000", part_1(example_data))

    def test_day1_part_1(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("71506", part_1(input_file.readlines()))

    def test_day1_part_2_example(self) -> None:
        self.assertEqual("45000", part_2(example_data))

    def test_day1_part_2(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("209603", part_2(input_file.readlines()))


if __name__ == '__main__':
    unittest.main()
