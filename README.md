# advent-of-code-2022
Python project for Advent of Code 2022

This project will auto populate the following files:
- `dayN.py` -- This file is where the logic goes, it will have a `part_1` and `part_2` function auto generated, with the signature of `list[str] -> str`
- `test_dayN.py` -- This file is where the testing goes, it will auto download the example and load the user specific input and execcute tests against both functions in `dayN.py`
- `input_dayN.txt` -- This stores user specific input

To generate these files, it is needed to:

- Create a `.config/session.json` file in the repo, which has a JSON object like `{ "sessionId": "12345" }`
- Run `bootstrapper.py`
