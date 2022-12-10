import unittest
import os
import days
from days.day10 import part_1, part_2

example_data = ["noop", "addx 3", "addx -5"]
days_dir = os.path.dirname(days.__file__)
input_file_name = os.path.join(days_dir, "input_day10.txt")
example_file_name = os.path.join(days_dir, "example_day10.txt")
example_image = """
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
""".strip()

input_image = """
####.#..#.####.####.####.#..#..##..####.
#....#..#....#.#.......#.#..#.#..#....#.
###..####...#..###....#..####.#......#..
#....#..#..#...#.....#...#..#.#.....#...
#....#..#.#....#....#....#..#.#..#.#....
####.#..#.####.#....####.#..#..##..####.
""".strip()


class TestDay10(unittest.TestCase):
    def test_day10_part_1_example(self) -> None:
        with open(example_file_name, "r") as example_file:
            self.assertEqual("13140", part_1(example_file.readlines()))

    def test_day10_part_1(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("14540", part_1(input_file.readlines()))

    def test_day10_part_2_example(self) -> None:
        with open(example_file_name, "r") as example_file:
            self.assertEqual(example_image, part_2(example_file.readlines()))

    def test_day10_part_2(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual(input_image, part_2(input_file.readlines()))


if __name__ == '__main__':
    unittest.main()
