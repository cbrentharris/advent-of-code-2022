import unittest
import os
import days
from days.day5 import part_1, part_2

example_data = ["    [D]    ", "[N] [C]    ", "[Z] [M] [P]", " 1   2   3 ", "", "move 1 from 2 to 1",
                "move 3 from 1 to 3", "move 2 from 2 to 1", "move 1 from 1 to 2"]
days_dir = os.path.dirname(days.__file__)
input_file_name = os.path.join(days_dir, "input_day5.txt")


class TestDay5(unittest.TestCase):
    def test_day5_part_1_example(self) -> None:
        self.assertEqual("CMZ", part_1(example_data))

    def test_day5_part_1(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("ZBDRNPMVH", part_1(input_file.readlines()))

    def test_day5_part_2_example(self) -> None:
        self.assertEqual("MCD", part_2(example_data))

    def test_day5_part_2(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("WDLPFNNNB", part_2(input_file.readlines()))


if __name__ == '__main__':
    unittest.main()
