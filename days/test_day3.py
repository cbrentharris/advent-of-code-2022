import unittest
import os
import days
from days.day3 import part_1, part_2

example_data = ["vJrwpWtwJgWrhcsFMMfFFhFp", "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL", "PmmdzqPrVvPwwTWBwg",
                "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn", "ttgJtRGJQctTZtZT", "CrZsJsPPZsGzwwsLwLmpwMDw"]
days_dir = os.path.dirname(days.__file__)
input_file_name = os.path.join(days_dir, "input_day3.txt")


class TestDay3(unittest.TestCase):
    def test_day3_part_1_example(self) -> None:
        self.assertEqual("157", part_1(example_data))

    def test_day3_part_1(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("7875", part_1(input_file.readlines()))

    def test_day3_part_2_example(self) -> None:
        self.assertEqual("70", part_2(example_data))

    def test_day3_part_2(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("2479", part_2(input_file.readlines()))


if __name__ == '__main__':
    unittest.main()
