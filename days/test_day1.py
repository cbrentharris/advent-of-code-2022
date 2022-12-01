
import unittest
from day1 import part_1, part_2

example_data = ["1000", "2000", "3000", "", "4000", "", "5000", "6000", "", "7000", "8000", "9000", "", "10000"]

class TestDay1(unittest.TestCase):
    def test_day1_part_1_example(self) -> None:
        self.assertEqual(part_1(example_data), "24000")

    def test_day1_part_1(self) -> None:
        with open("./input_day1.txt", "r") as input_file:
            self.assertEqual(part_1(input_file.readlines()), "71506")

    def test_day1_part_2_example(self) -> None:
        self.assertEqual(part_2(example_data), "45000")

    def test_day1_part_2(self) -> None:
        with open("./input_day1.txt", "r") as input_file:
            self.assertEqual(part_2(input_file.readlines()), "209603")

if __name__ == '__main__':
    unittest.main()
