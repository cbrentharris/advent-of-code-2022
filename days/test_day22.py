import unittest
import os
import days
from days.day22 import part_1, part_2

example_data = ["        ...#", "        .#..", "        #...", "        ....", "...#.......#", "........#...", "..#....#....", "..........#.", "        ...#....", "        .....#..", "        .#......", "        ......#.", "", "10R5L5R10L4R5L5"]
days_dir = os.path.dirname(days.__file__)
input_file_name = os.path.join(days_dir, "input_day22.txt")


class TestDay22(unittest.TestCase):
    def test_day22_part_1_example(self) -> None:
        self.assertEqual("6032", part_1(example_data))

    def test_day22_part_1(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("55244", part_1(input_file.readlines()))

    def test_day22_part_2_example(self) -> None:
        self.assertEqual("", part_2(example_data))

    def test_day22_part_2(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("", part_2(input_file.readlines()))


if __name__ == '__main__':
    unittest.main()
