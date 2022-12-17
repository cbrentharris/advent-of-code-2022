import unittest
import os
import days
from days.day16 import part_1, part_2

example_data = ["Valve AA has flow rate=0; tunnels lead to valves DD, II, BB", "Valve BB has flow rate=13; tunnels lead to valves CC, AA", "Valve CC has flow rate=2; tunnels lead to valves DD, BB", "Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE", "Valve EE has flow rate=3; tunnels lead to valves FF, DD", "Valve FF has flow rate=0; tunnels lead to valves EE, GG", "Valve GG has flow rate=0; tunnels lead to valves FF, HH", "Valve HH has flow rate=22; tunnel leads to valve GG", "Valve II has flow rate=0; tunnels lead to valves AA, JJ", "Valve JJ has flow rate=21; tunnel leads to valve II"]
days_dir = os.path.dirname(days.__file__)
input_file_name = os.path.join(days_dir, "input_day16.txt")


class TestDay16(unittest.TestCase):
    def test_day16_part_1_example(self) -> None:
        self.assertEqual("1651", part_1(example_data))

    def test_day16_part_1(self) -> None:
        with open(input_file_name, "r") as input_file:
            input_lines = input_file.readlines()
            result = part_1(input_lines)
            self.assertNotEqual("1848", result)
            self.assertEqual("1584", result)

    def test_day16_part_2_example(self) -> None:
        self.assertEqual("", part_2(example_data))

    def test_day16_part_2(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("", part_2(input_file.readlines()))


if __name__ == '__main__':
    unittest.main()
