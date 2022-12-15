import unittest
import os
import days
from days.day15 import part_1, part_2

example_data = ["Sensor at x=2, y=18: closest beacon is at x=-2, y=15",
                "Sensor at x=9, y=16: closest beacon is at x=10, y=16",
                "Sensor at x=13, y=2: closest beacon is at x=15, y=3",
                "Sensor at x=12, y=14: closest beacon is at x=10, y=16",
                "Sensor at x=10, y=20: closest beacon is at x=10, y=16",
                "Sensor at x=14, y=17: closest beacon is at x=10, y=16",
                "Sensor at x=8, y=7: closest beacon is at x=2, y=10",
                "Sensor at x=2, y=0: closest beacon is at x=2, y=10",
                "Sensor at x=0, y=11: closest beacon is at x=2, y=10",
                "Sensor at x=20, y=14: closest beacon is at x=25, y=17",
                "Sensor at x=17, y=20: closest beacon is at x=21, y=22",
                "Sensor at x=16, y=7: closest beacon is at x=15, y=3",
                "Sensor at x=14, y=3: closest beacon is at x=15, y=3",
                "Sensor at x=20, y=1: closest beacon is at x=15, y=3"]
days_dir = os.path.dirname(days.__file__)
input_file_name = os.path.join(days_dir, "input_day15.txt")


class TestDay15(unittest.TestCase):
    def test_day15_part_1_example(self) -> None:
        self.assertEqual("26", part_1(example_data, 10))

    def test_day15_part_1(self) -> None:
        with open(input_file_name, "r") as input_file:
            lines = input_file.readlines()
            self.assertNotEqual("2645610", part_1(lines, 2000000))
            self.assertNotEqual("5108307", part_1(lines, 2000000))
            self.assertNotEqual("8785479", part_1(lines, 2000000))
            self.assertNotEqual("9194420", part_1(lines, 2000000))
            self.assertEqual("5040643", part_1(lines, 2000000))

    def test_day15_part_2_example(self) -> None:
        self.assertEqual("56000011", part_2(example_data, 0, 20))

    def test_day15_part_2(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("11016575214126", part_2(input_file.readlines(), 0, 4000000))


if __name__ == '__main__':
    unittest.main()
