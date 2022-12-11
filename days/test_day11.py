import unittest
import os
import days
from days.day11 import part_1, part_2

example_data = [
    "Monkey 0:",
    "  Starting items: 79, 98",
    "  Operation: new = old * 19",
    "  Test: divisible by 23",
    "    If true: throw to monkey 2",
    "    If false: throw to monkey 3",
    "",
    "Monkey 1:",
    "  Starting items: 54, 65, 75, 74",
    "  Operation: new = old + 6",
    "  Test: divisible by 19",
    "    If true: throw to monkey 2",
    "    If false: throw to monkey 0",
    "",
    "Monkey 2:",
    "  Starting items: 79, 60, 97",
    "  Operation: new = old * old",
    "  Test: divisible by 13",
    "    If true: throw to monkey 1",
    "    If false: throw to monkey 3",
    "",
    "Monkey 3:",
    "  Starting items: 74",
    "  Operation: new = old + 3",
    "  Test: divisible by 17",
    "    If true: throw to monkey 0",
    "    If false: throw to monkey 1"
]
days_dir = os.path.dirname(days.__file__)
input_file_name = os.path.join(days_dir, "input_day11.txt")


class TestDay11(unittest.TestCase):
    def test_day11_part_1_example(self) -> None:
        self.assertEqual("10605", part_1(example_data))

    def test_day11_part_1(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("58322", part_1(input_file.readlines()))

    def test_day11_part_2_example(self) -> None:
        self.assertEqual("2713310158", part_2(example_data))

    def test_day11_part_2(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("13937702909", part_2(input_file.readlines()))


if __name__ == '__main__':
    unittest.main()
