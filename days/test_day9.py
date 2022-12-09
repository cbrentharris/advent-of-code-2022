import unittest
import os
import days
from days.day9 import part_1, part_2

example_data = [
    "R 4",
    "U 4",
    "L 3",
    "D 1",
    "R 4",
    "D 1",
    "L 5",
    "R 2",
]

larger_example = [
    "R 5",
    "U 8",
    "L 8",
    "D 3",
    "R 17",
    "D 10",
    "L 25",
    "U 20",
]
days_dir = os.path.dirname(days.__file__)
input_file_name = os.path.join(days_dir, "input_day9.txt")


class TestDay9(unittest.TestCase):
    def test_day9_part_1_example(self) -> None:
        self.assertEqual("13", part_1(example_data))

    def test_day9_part_1(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("6311", part_1(input_file.readlines()))

    def test_day9_part_2_example(self) -> None:
        self.assertEqual("36", part_2(larger_example))

    def test_day9_part_2(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("2482", part_2(input_file.readlines()))


if __name__ == '__main__':
    unittest.main()
