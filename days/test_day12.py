import unittest
import os
import days
from days.day12 import part_1, part_2

example_data = ["Sabqponm", "abcryxxl", "accszExk", "acctuvwj", "abdefghi"]
days_dir = os.path.dirname(days.__file__)
input_file_name = os.path.join(days_dir, "input_day12.txt")


class TestDay12(unittest.TestCase):
    def test_day12_part_1_example(self) -> None:
        self.assertEqual("31", part_1(example_data))

    def test_day12_part_1(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("520", part_1(input_file.readlines()))

    def test_day12_part_2_example(self) -> None:
        self.assertEqual("29", part_2(example_data))

    def test_day12_part_2(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("508", part_2(input_file.readlines()))


if __name__ == '__main__':
    unittest.main()
