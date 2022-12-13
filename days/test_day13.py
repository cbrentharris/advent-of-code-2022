import unittest
import os
import days
from days.day13 import part_1, part_2

example_data = ["[1,1,3,1,1]", "[1,1,5,1,1]", "", "[[1],[2,3,4]]", "[[1],4]", "", "[9]", "[[8,7,6]]", "", "[[4,4],4,4]",
                "[[4,4],4,4,4]", "", "[7,7,7,7]", "[7,7,7]", "", "[]", "[3]", "", "[[[]]]", "[[]]", "",
                "[1,[2,[3,[4,[5,6,7]]]],8,9]", "[1,[2,[3,[4,[5,6,0]]]],8,9]"]
days_dir = os.path.dirname(days.__file__)
input_file_name = os.path.join(days_dir, "input_day13.txt")


class TestDay13(unittest.TestCase):
    def test_day13_part_1_example(self) -> None:
        self.assertEqual("13", part_1(example_data))

    def test_day13_part_1(self) -> None:
        with open(input_file_name, "r") as input_file:
            part_1_answer = part_1(input_file.readlines())
            self.assertNotEqual("5904", part_1_answer)
            self.assertNotEqual("5819", part_1_answer)
            self.assertEqual("5625", part_1_answer)

    def test_day13_part_2_example(self) -> None:
        self.assertEqual("", part_2(example_data))

    def test_day13_part_2(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("", part_2(input_file.readlines()))


if __name__ == '__main__':
    unittest.main()
