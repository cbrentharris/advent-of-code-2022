"""
Tuning Trouble
"""


def part_1(datastream: list[str]) -> str:
    return find_character_marker(datastream[0], 4)


def part_2(datastream: list[str]) -> str:
    return find_character_marker(datastream[0], 14)


def find_character_marker(unwrapped_datastream: str, num_unique_chars: int) -> str:
    start = 0
    while len(set(unwrapped_datastream[start:start + num_unique_chars])) != num_unique_chars:
        start += 1
    return str(start + num_unique_chars)
