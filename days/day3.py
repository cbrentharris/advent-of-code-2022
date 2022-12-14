from functools import reduce
from typing import Iterable

from days.local_functools import chunk

"""
Rucksack Reorganization
"""


def part_1(rucksack_organization: list[str]) -> str:
    def splitter(rucksack: str) -> (str, str):
        rucksack_midpoint = int(len(rucksack) / 2)
        return rucksack[:rucksack_midpoint], rucksack[rucksack_midpoint:]

    split = map(splitter, rucksack_organization)

    def common_letter_finder(rucksack_halves: (str, str)) -> str:
        return (set(rucksack_halves[0]) & set(rucksack_halves[1])).pop()

    common_letters = map(common_letter_finder, split)

    ordinal_values = map(prioritization_valuer, common_letters)
    return str(sum(ordinal_values))


def part_2(rucksacks: list[str]) -> str:
    chunked = chunk(rucksacks, 3)

    def common_element_finder(grouped: Iterable[str]) -> str:
        return reduce(lambda a, b: a.intersection(b), map(set, map(lambda x: x.strip(), grouped))).pop()

    common_elements = map(common_element_finder, chunked)

    ordinal_values = map(prioritization_valuer, common_elements)

    return str(sum(ordinal_values))


def prioritization_valuer(c: str) -> int:
    return (ord(c) - ord('a') if c.islower() else ord(c) - ord('A') + 26) + 1
