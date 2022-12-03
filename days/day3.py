from functools import reduce
from typing import Iterable

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
    def chunk(l: list[str], n: int) -> Iterable[Iterable[str]]:
        for i in range(0, len(l), n):
            yield l[i:i + n]

    chunked = chunk(rucksacks, 3)

    def common_element_finder(grouped: Iterable[str]) -> str:
        return reduce(lambda a, b: a.intersection(b), map(set, map(lambda x: x.strip(), grouped))).pop()

    common_elements = map(common_element_finder, chunked)

    ordinal_values = map(prioritization_valuer, common_elements)

    return str(sum(ordinal_values))


def prioritization_valuer(c: str) -> int:
    return ord(c) - 96 if c.islower() else ord(c) - 64 + 26
