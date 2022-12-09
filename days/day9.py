"""
Rope Bridge
"""

UP = "U"
DOWN = "D"
LEFT = "L"
RIGHT = "R"


class Instruction(object):
    def __init__(self, raw_direction: str):
        direction, steps = raw_direction.strip().split(" ")
        self.direction = direction
        self.steps = int(steps)

    def __repr__(self):
        return str(self.direction) + str(self.steps)


class Knot(object):
    def __init__(self, pos: [int, int], tail=None):
        self.pos = pos
        self.tail = tail

    def __repr__(self):
        return str(self.pos) + " " + str(self.tail)

    def move(self, direction: str):
        x, y = self.pos
        if direction == UP:
            self.pos = x, y + 1
        elif direction == DOWN:
            self.pos = x, y - 1
        elif direction == RIGHT:
            self.pos = x + 1, y
        else:
            self.pos = x - 1, y

        if self.tail is not None:
            self.tail.follow(self.pos)

    def follow(self, pos: [int, int]) -> None:
        if self.is_adjacent(pos):
            return

        x, y = self.pos
        deltas = set([(i, j) for i in range(-1, 2) for j in range(-1, 2)])
        possible_moves = map(lambda delta: (x + delta[0], y + delta[1]), deltas)
        self.pos = min(possible_moves, key=lambda p: manhattan_distance(p, pos))
        if self.tail is not None:
            self.tail.follow(self.pos)

    def is_adjacent(self, pos: [int, int]) -> bool:
        x, y = pos
        self_x, self_y = self.pos
        return abs(x - self_x) <= 1 and abs(y - self_y) <= 1


def manhattan_distance(a: [int, int], b: [int, int]) -> int:
    a_x, a_y = a
    b_x, b_y = b
    return abs(a_x - b_x) + abs(a_y - b_y)


def part_1(raw_directions: list[str]) -> str:
    instructions = map(Instruction, raw_directions)
    initial_pos = (0, 0)
    visited_tail_positions = set()
    visited_tail_positions.add(initial_pos)
    head = Knot(initial_pos, Knot(initial_pos))
    tail = head.tail
    for instruction in instructions:
        for _ in range(instruction.steps):
            head.move(instruction.direction)
            visited_tail_positions.add(tail.pos)

    return str(len(visited_tail_positions))


def part_2(raw_directions: list[str]) -> str:
    instructions = map(Instruction, raw_directions)
    initial_pos = (0, 0)
    visited_tail_positions = set()
    visited_tail_positions.add(initial_pos)
    head = Knot(initial_pos, Knot(initial_pos))
    curr = head
    for i in range(8):
        curr = curr.tail
        curr.tail = Knot(initial_pos)
    tail = curr.tail

    for instruction in instructions:
        for _ in range(instruction.steps):
            head.move(instruction.direction)
            visited_tail_positions.add(tail.pos)

    return str(len(visited_tail_positions))
