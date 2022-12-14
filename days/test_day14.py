import unittest
import os
import days
from days.day14 import part_1, part_2

example_data = ["498,4 -> 498,6 -> 496,6", "503,4 -> 502,4 -> 502,9 -> 494,9"]
days_dir = os.path.dirname(days.__file__)
input_file_name = os.path.join(days_dir, "input_day14.txt")


class TestDay14(unittest.TestCase):
    def test_day14_part_1_example(self) -> None:
        self.assertEqual("24", part_1(example_data))

    def test_day14_part_1(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("1513", part_1(input_file.readlines()))

    def test_day14_part_2_example(self) -> None:
        self.assertEqual("93", part_2(example_data))

    def test_day14_part_2(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("22646", part_2(input_file.readlines()))


if __name__ == '__main__':
    unittest.main()
