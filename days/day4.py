"""
Camp Cleanup
"""


def part_1(sections: list[str]) -> str:
    parsed = map(parse_sections, sections)
    return str(len(list(filter(is_completely_overlapping, parsed))))


def parse_sections(sections: str) -> ((int, int), (int, int)):
    first, second = sections.split(",")

    def parse_section(section: str) -> (int, int):
        start, end = section.split("-")
        return int(start), int(end)

    return parse_section(first), parse_section(second)


def is_completely_overlapping(sections: ((int, int), (int, int))) -> bool:
    first, second = sections
    return contains(first, second) or contains(second, first)


def contains(a: (int, int), b: (int, int)):
    return a[0] <= b[0] and a[1] >= b[1]


def part_2(sections: list[str]) -> str:
    parsed = map(parse_sections, sections)
    return str(len(list(filter(is_overlapping, parsed))))


def is_overlapping(sections: ((int, int), (int, int))) -> bool:
    first, second = sections
    return overlaps(first, second) or overlaps(second, first)


def overlaps(a: (int, int), b: (int, int)):
    return a[0] <= b[0] <= a[1]
