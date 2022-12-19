import unittest
import os
import days
from days.day17 import part_1, part_2

example_data = [">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"]
days_dir = os.path.dirname(days.__file__)
input_file_name = os.path.join(days_dir, "input_day17.txt")


class TestDay17(unittest.TestCase):
    def test_day17_part_1_example(self) -> None:
        self.assertEqual("3068", part_1(example_data))

    def test_day17_part_1(self) -> None:
        with open(input_file_name, "r") as input_file:
            answer = part_1(input_file.readlines())
            self.assertNotEqual("3145", answer)
            self.assertEqual("3127", answer)

    def test_day17_part_2_example(self) -> None:
        self.assertEqual("1514285714288", part_2(example_data))

    def test_day17_part_2(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("1542941176480", part_2(input_file.readlines()))


if __name__ == '__main__':
    unittest.main()
