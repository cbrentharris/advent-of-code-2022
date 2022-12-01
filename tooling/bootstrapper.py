import os
import days
from aocd.models import Puzzle, User
from datetime import date
import json
from pathlib import Path

day_template = """\"\"\"
{title}
\"\"\"
def part_1(input: list[str]) -> str:
    return ""

def part_2(input: list[str]) -> str:
    return ""
"""

test_day_template = """import unittest
import os
import days
from days.day{day} import part_1, part_2

example_data = {example_data}
days_dir = os.path.dirname(days.__file__)
input_file_name = os.path.join(days_dir, "input_day{day}.txt")


class TestDay{day}(unittest.TestCase):
    def test_day{day}_part_1_example(self) -> None:
        self.assertEqual("", part_1(example_data))

    def test_day{day}_part_1(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("", part_1(input_file.readlines()))

    def test_day{day}_part_2_example(self) -> None:
        self.assertEqual("", part_2(example_data))

    def test_day{day}_part_2(self) -> None:
        with open(input_file_name, "r") as input_file:
            self.assertEqual("", part_2(input_file.readlines()))


if __name__ == '__main__':
    unittest.main()
"""
def create_day_files(current_day = date.today(), session=None):
    day_num = str(current_day.day)
    days_dir = os.path.dirname(days.__file__)
    day_input_file_name = os.path.join(days_dir, "input_day" + day_num + ".txt")
    days_file_name = os.path.join(days_dir, "day" + day_num + ".py")
    test_days_file_name = os.path.join(days_dir, "test_day" + day_num + ".py")

    puzzle = Puzzle(year=current_day.year, day=current_day.day, user=User(session))

    if any(map(os.path.exists, [days_file_name, days_file_name, test_days_file_name])):
        raise Exception("Files already exist")
    with open(days_file_name, 'w') as days_file:
        days_file.write(day_template.format(title=puzzle.title))
    with open(test_days_file_name, 'w') as test_days_file:
        test_days_file.write(test_day_template.format(day=day_num, example_data=json.dumps(puzzle.example_data.split("\n"))))

    with open(day_input_file_name, 'w') as input_file:
        input_file.write(puzzle.input_data)

if __name__ == "__main__":
    days_path = Path(os.path.dirname(days.__file__))
    session_id = json.load(open(os.path.join(str(days_path.parent), ".config", "session.json"), "r"))["sessionId"]
    create_day_files(session=session_id)
