import unittest
import os
import days
from days.day7 import part_1, part_2

example_data = [
    "$ cd /",
    "$ ls",
    "dir a",
    "14848514 b.txt",
    "8504156 c.dat",
    "dir d",
    "$ cd a",
    "$ ls",
    "dir e",
    "29116 f",
    "2557 g",
    "62596 h.lst",
    "$ cd e",
    "$ ls",
    "584 i",
    "$ cd ..",
    "$ cd ..",
    "$ cd d",
    "$ ls",
    "4060174 j",
    "8033020 d.log",
    "5626152 d.ext",
    "7214296 k"
]
days_dir = os.path.dirname(days.__file__)
input_file_name = os.path.join(days_dir, "input_day7.txt")


class TestDay7(unittest.TestCase):
    def test_day7_part_1_example(self) -> None:
        self.assertEqual("95437", part_1(example_data))

    def test_day7_part_1(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("1644735", part_1(input_file.readlines()))

    def test_day7_part_2_example(self) -> None:
        self.assertEqual("24933642", part_2(example_data))

    def test_day7_part_2(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("1300850", part_2(input_file.readlines()))


if __name__ == '__main__':
    unittest.main()
