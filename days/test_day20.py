import unittest
import os
import days
from days.day20 import part_1, part_2, Node, Decrypter

example_data = ["1", "2", "-3", "3", "-2", "0", "4"]
days_dir = os.path.dirname(days.__file__)
input_file_name = os.path.join(days_dir, "input_day20.txt")


class TestDay20(unittest.TestCase):
    def test_day20_part_1_example(self) -> None:
        self.assertEqual("3", part_1(example_data))

    def test_day20_part_1(self) -> None:
        with open(input_file_name, "r") as input_file:
            answer = int(part_1(input_file.readlines()))
            self.assertLess(-944, answer)
            self.assertLess(4191, answer)
            self.assertGreater(9174, answer)
            self.assertGreater(7976, answer)
            self.assertEqual(5498, answer)

    def test_day20_part_2_example(self) -> None:
        self.assertEqual("1623178306", part_2(example_data))

    def test_day20_part_2(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("3390007892081", part_2(input_file.readlines()))


if __name__ == '__main__':
    unittest.main()
