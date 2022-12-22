import unittest
import os
import days
from days.day19 import part_1, part_2

example_data = [
    "Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 "
    "clay. Each geode robot costs 2 ore and 7 obsidian.",
    "Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 "
    "clay. Each geode robot costs 3 ore and 12 obsidian."]
days_dir = os.path.dirname(days.__file__)
input_file_name = os.path.join(days_dir, "input_day19.txt")


class TestDay19(unittest.TestCase):
    def test_day19_part_1_example(self) -> None:
        self.assertEqual("33", part_1(example_data))

    def test_day19_part_1(self) -> None:
        with open(input_file_name, "r") as input_file:
            answer = part_1(input_file.readlines())
            self.assertLess("1711", answer, "1711 Was too low last time.")
            self.assertEqual("1719", answer)

    def test_day19_part_2_example(self) -> None:
        self.assertEqual("3042", part_2(example_data))

    def test_day19_part_2(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("19530", part_2(input_file.readlines()))


if __name__ == '__main__':
    unittest.main()
