"""
Monkey Map
"""


class Steps(object):
    def __init__(self):
        pass


class Grid(object):
    OPEN_TILE = "."
    VOID = ""
    WALL = "#"
    UP = "U"
    DOWN = "D"
    RIGHT = "R"
    LEFT = "L"

    FACING_SCORE = {
        RIGHT: 0,
        DOWN: 1,
        LEFT: 2,
        UP: 3
    }

    NEXT_DIRECTION = {
        LEFT: {
            UP: LEFT,
            LEFT: DOWN,
            DOWN: RIGHT,
            RIGHT: UP
        },
        RIGHT: {
            UP: RIGHT,
            RIGHT: DOWN,
            DOWN: LEFT,
            LEFT: UP
        }
    }

    def __init__(self, map_tiles: list[str]):
        self.max_width = max(map(len, map_tiles))
        self.rows = []
        for raw_row in map_tiles:
            row = [square.strip() for square in list(raw_row)] + [''] * (self.max_width - len(raw_row))
            self.rows.append(row)
        self.x = 0
        self.y = self.find_first_nonempty_index(self.rows[0])
        self.facing = Grid.RIGHT

    @staticmethod
    def find_first_nonempty_index(row: list[str], reverse=False):
        enumerated = reversed(list(enumerate(row))) if reverse else enumerate(row)
        return next(i for i, r in enumerated if r != Grid.VOID)

    def move(self, steps: int) -> None:
        if self.moving_horizontally():
            self.move_horizontally(steps)
        else:
            self.move_vertically(steps)

    def move_horizontally(self, steps: int) -> None:
        current_row = self.rows[self.x]
        current_column_index = self.y
        steps_taken = 0
        while steps_taken < steps:
            if self.facing == Grid.RIGHT:
                next_space_index = current_column_index + 1
                if next_space_index >= self.max_width or self.current_row()[next_space_index] == Grid.VOID:
                    next_space_index = self.find_first_nonempty_index(self.current_row())
            else:
                next_space_index = current_column_index - 1
                if next_space_index == - 1 or self.current_row()[next_space_index] == Grid.VOID:
                    next_space_index = self.find_first_nonempty_index(self.current_row(), reverse=True)

            next_space = current_row[next_space_index]
            if next_space == Grid.WALL:
                break
            current_column_index = next_space_index
            steps_taken += 1
        self.y = current_column_index

    def move_vertically(self, steps: int):
        current_row_index = self.x
        steps_taken = 0
        while steps_taken < steps:
            if self.facing == Grid.UP:
                next_row_index = current_row_index - 1
                if next_row_index < 0 or self.rows[next_row_index][self.y] == Grid.VOID:
                    next_row_index = self.find_first_nonempty_index_along_column(reverse=True)
            else:
                next_row_index = current_row_index + 1
                if next_row_index >= len(self.rows) or self.rows[next_row_index][self.y] == Grid.VOID:
                    next_row_index = self.find_first_nonempty_index_along_column()
            next_space = self.rows[next_row_index][self.y]
            if next_space == Grid.WALL:
                break
            current_row_index = next_row_index
            steps_taken += 1
        self.x = current_row_index

    def moving_horizontally(self):
        return self.facing == Grid.LEFT or self.facing == Grid.RIGHT

    def current_row(self):
        return self.rows[self.x]

    def find_first_nonempty_index_along_column(self, reverse=False):
        range_to_iterate = range(len(self.rows))
        if reverse:
            range_to_iterate = reversed(range_to_iterate)
        return next(i for i in range_to_iterate if self.rows[i][self.y] != Grid.VOID)

    def turn(self, direction):
        self.facing = Grid.NEXT_DIRECTION[direction][self.facing]

    def score(self):
        return (self.x + 1) * 1000 + (self.y + 1) * 4 + Grid.FACING_SCORE[self.facing]


def parse_directions(direction_str: str):
    output = []
    acc = ""
    for s in direction_str:
        if s.isdigit():
            acc = acc + s
        else:
            output.append(int(acc))
            acc = ""
            output.append(s)
    return output


def part_1(raw_input: list[str]) -> str:
    map_tiles = raw_input[:len(raw_input) - 2]
    directions = parse_directions(raw_input[-1])
    grid = Grid(map_tiles)
    for d in directions:
        if type(d) == int:
            grid.move(d)
        else:
            grid.turn(d)
    return str(grid.score())


def part_2(input: list[str]) -> str:
    return ""
