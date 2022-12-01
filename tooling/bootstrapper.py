import os
import days
from aocd import get_data
from datetime import date

day_template = """
\"\"\"
A stub method to execute for the new aoc day
\"\"\"
def main(input):
    pass
"""

test_day_template = """
import unittest
from {day} import main

class TestDay{day}(unittest.TestCase):
    def test_day{day}(self):
        with open("./input_day{day}.txt", "w") as input_file:
            main(input_file.readlines())

if __name__ == '__main__':
    unittest.main()
"""
def create_day_files(current_day = date.today(), session=None):
    day_num = current_day.day
    days_dir = os.path.dirname(days.__file__)
    day_input_file_name = os.path.join(days_dir, "input_day" + day_num + ".txt")
    days_file_name = os.path.join(days_dir, "day" + day_num + ".py")
    test_days_file_name = os.path.join(days_dir, "test_day" + day_num + ".py")

    if any(map(os.path.exists, [days_file_name, days_file_name, test_days_file_name])):
        raise Exception("Files already exist")
    with open(days_file_name, 'w') as days_file:
        days_file.write(day_template)
    with open(test_days_file_name, 'w') as test_days_file:
        test_days_file.write(test_day_template)

    with open(day_input_file_name, 'w') as input_file:
        input_file.write(get_data(year=current_day.year, day=current_day.day, session=session))