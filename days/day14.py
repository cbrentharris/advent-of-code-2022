"""
Regolith Reservoir
"""


class Line(object):
    def __init__(self, pairs: list[list[int]]):
        first, second = pairs
        first_x, first_y = first
        second_x, second_y = second
        self.first_x = first_x
        self.first_y = first_y
        self.second_x = second_x
        self.second_y = second_y
        self.first = (first_x, first_y)
        self.second = (second_x, second_y)
        self.pairs = frozenset([self.first, self.second])

    def points(self):
        if self.is_horizontal():
            start, stop = sorted([self.first_x, self.second_x])
            for i in range(start, stop + 1):
                yield i, self.first_y
        else:
            start, stop = sorted([self.first_y, self.second_y])
            for i in range(start, stop + 1):
                yield self.first_x, i

    def is_horizontal(self):
        return self.first_y == self.second_y

    def __hash__(self):
        return hash(self.pairs)

    def __repr__(self):
        return " : ".join(map(str, [self.first, self.second]))


def parse_lines(path_str: str) -> set[Line]:
    string_pairs = path_str.split(" -> ")
    pairs = list(map(lambda string_pair: list(map(int, string_pair.split(","))), string_pairs))
    return set(map(Line, [pairs[start:start + 2] for start in range(0, len(pairs) - 1)]))


def find_next_point(points, current_point):
    x, y = current_point
    down = x, y + 1
    down_left = x - 1, y + 1
    down_right = x + 1, y + 1
    for point in [down, down_left, down_right]:
        if point not in points:
            return point
    return current_point


def part_1(raw_rock_paths: list[str]) -> str:
    rock_paths = set([line for lines in map(parse_lines, raw_rock_paths) for line in lines])
    rock_points = set([point for line in rock_paths for point in line.points()])
    starting_point = (500, 0)
    into_the_abyss = False
    current_point = starting_point
    sand = set()
    lowest_point = max(map(lambda p: p[1], rock_points))
    while not into_the_abyss:
        next_point = find_next_point(rock_points, current_point)
        if next_point == current_point:
            rock_points.add(current_point)
            sand.add(current_point)
            current_point = starting_point
            continue
        current_point = next_point
        _, y = current_point
        if y > lowest_point:
            into_the_abyss = True

    return str(len(sand))


def part_2(raw_rock_paths: list[str]) -> str:
    rock_paths = set([line for lines in map(parse_lines, raw_rock_paths) for line in lines])
    rock_points = set([point for line in rock_paths for point in line.points()])
    starting_point = (500, 0)
    at_the_top = False
    current_point = starting_point
    sand = set()
    lowest_point = max(map(lambda p: p[1], rock_points)) + 2
    while not at_the_top:
        next_point = find_next_point(rock_points, current_point)
        _, y = current_point
        if next_point == current_point == starting_point:
            at_the_top = True
        if next_point == current_point or y == lowest_point - 1:
            rock_points.add(current_point)
            sand.add(current_point)
            current_point = starting_point
            continue
        current_point = next_point

    return str(len(sand))
