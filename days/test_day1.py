import unittest
from day1 import part_1, part_2

class TestDay1(unittest.TestCase):
    def test_day1(self):
        with open("./input_day1.txt", "r") as input_file:
            self.assertEqual(part_1(input_file.readlines()), 71506)

    def test_day2(self):
        with open("./input_day1.txt", "r") as input_file:
            self.assertEqual(part_2(input_file.readlines()), 209603)

if __name__ == '__main__':
    unittest.main()
