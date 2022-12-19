"""
Pyroclastic Flow
"""
import itertools

CHAMBER_WIDTH = 7
CHAMBER_OFFSET_HEIGHT = 3
EMPTY_CHARACTER = "."


class RockShape(object):
    LEFT = "<"
    RIGHT = ">"

    def __init__(self, grid: list[list], running_grid: list[list], maximums: list[int]):
        self.grid = grid
        self.max_height = len(grid)
        self.max_width = max(map(len, grid))
        self.running_grid = running_grid
        self.x_offset = 2
        self.y_offset = len(running_grid) + CHAMBER_OFFSET_HEIGHT
        self.maximums = maximums

    def push(self, direction: str) -> None:
        if direction == RockShape.LEFT:
            self.try_move_left()
        elif direction == RockShape.RIGHT:
            self.try_move_right()

    def is_not_on_top_of_any_shape(self) -> bool:
        for row_index in self.get_row_range():
            if row_index >= len(self.running_grid):
                continue
            running_grid_row = self.running_grid[row_index]
            local_row = self.grid[row_index - self.y_offset]
            for column_index in self.get_column_range():
                running_grid_column = running_grid_row[column_index]
                if running_grid_column is None:
                    continue
                local_column = local_row[column_index - self.x_offset]
                if local_column is None:
                    continue
                return False
        return True

    def get_row_range(self) -> range:
        row_start = self.y_offset
        row_end = self.y_offset + self.max_height
        return range(row_start, row_end)

    def get_column_range(self) -> range:
        column_start = self.x_offset
        column_end = self.x_offset + self.max_width
        return range(column_start, column_end)

    def try_move_left(self) -> None:
        if self.x_offset == 0:
            return
        self.x_offset -= 1
        if self.is_not_on_top_of_any_shape():
            return
        self.x_offset += 1

    def try_move_right(self) -> None:
        if self.x_offset + self.max_width == CHAMBER_WIDTH:
            return
        self.x_offset += 1
        if self.is_not_on_top_of_any_shape():
            return
        self.x_offset -= 1

    def place_in_grid(self) -> None:
        for row_index in self.get_row_range():
            if len(self.running_grid) == row_index:
                self.running_grid.append([None] * CHAMBER_WIDTH)
            row = self.running_grid[row_index]
            for column_index in self.get_column_range():
                column = self.grid[row_index - self.y_offset][column_index - self.x_offset]
                if column is None:
                    continue
                self.maximums[column_index] = max(self.maximums[column_index], row_index)
                row[column_index] = column

    def try_move_down(self):
        if self.y_offset == 0:
            return False
        self.y_offset -= 1
        if self.is_not_on_top_of_any_shape():
            return True
        self.y_offset += 1
        return False


def part_1(jet_stream: list[str]) -> str:
    return height_after_rocks(2022, jet_stream)


def part_2(jet_stream: list[str]) -> str:
    num_rocks_to_fall = 1000000000000
    return height_after_rocks(num_rocks_to_fall, jet_stream)


def height_after_rocks(num_rocks_to_fall: int, jet_stream: list[str]):
    tokenized_jet_stream = list(jet_stream[0].strip())
    repeating_jetstream = itertools.cycle(tokenized_jet_stream)
    running_grid = []
    rocks_fallen = 0
    repeating_rocks = itertools.cycle(shapes())
    maximums = [0] * CHAMBER_WIDTH
    total = 0
    truncated_grids = set()
    height_after_rock_fallen = {0: 0}
    rocks_fallen_after_truncated_grid = {}
    jet_stream_offset_per_truncated_grid = {}
    pushes = 0
    has_detected_cycle = False
    while not has_detected_cycle and rocks_fallen < num_rocks_to_fall:
        direction = next(repeating_jetstream)
        next_rock = RockShape(next(repeating_rocks), running_grid, maximums)
        directions = [direction]
        next_rock.push(direction)
        pushes += 1
        moved_down = next_rock.try_move_down()
        while moved_down:
            direction = next(repeating_jetstream)
            next_rock.push(direction)
            pushes += 1
            directions.append(direction)
            moved_down = next_rock.try_move_down()
        next_rock.place_in_grid()
        rocks_fallen += 1
        min_row = min(maximums)
        running_grid = running_grid[min_row:]
        maximums = list(map(lambda x: x - min_row, maximums))
        total += min_row
        height_after_rock_fallen[rocks_fallen] = total + len(running_grid)
        stringified_truncated_grid = pretty_string(running_grid)
        jet_stream_offset = pushes % len(tokenized_jet_stream)
        has_detected_cycle = stringified_truncated_grid in truncated_grids and jet_stream_offset == \
                             jet_stream_offset_per_truncated_grid[stringified_truncated_grid]
        if has_detected_cycle:
            cycle_start = rocks_fallen_after_truncated_grid[stringified_truncated_grid]
            cycle_end = rocks_fallen
            cycle_width = cycle_end - cycle_start
            rocks_fallen_at_cycle_start = rocks_fallen_after_truncated_grid[stringified_truncated_grid]
            num_rocks_to_fall_offset = num_rocks_to_fall - rocks_fallen_at_cycle_start
            num_cycles = num_rocks_to_fall_offset // cycle_width
            rocks_to_fall_after_last_cycle = num_rocks_to_fall_offset % cycle_width
            height_at_cycle_start = height_after_rock_fallen[cycle_start]
            height_after_last_cycle = height_after_rock_fallen[
                                          cycle_start + rocks_to_fall_after_last_cycle] - height_at_cycle_start
            cycle_height = height_after_rock_fallen[cycle_end] - height_after_rock_fallen[cycle_start]
            total_height = cycle_height * num_cycles + height_at_cycle_start + height_after_last_cycle
            return str(total_height)
        truncated_grids.add(stringified_truncated_grid)
        rocks_fallen_after_truncated_grid[stringified_truncated_grid] = rocks_fallen
        jet_stream_offset_per_truncated_grid[stringified_truncated_grid] = pushes % len(tokenized_jet_stream)
    return str(height_after_rock_fallen[num_rocks_to_fall])


def shapes() -> list[list[list]]:
    return [
        [
            ["#", "#", "#", "#"]
        ],
        [
            [None, "#", None],
            ["#", "#", "#"],
            [None, "#", None],
        ],
        [
            ["#", "#", "#"],
            [None, None, "#"],
            [None, None, "#"],
        ],
        [
            ["#"],
            ["#"],
            ["#"],
            ["#"],
        ],
        [
            ["#", "#"],
            ["#", "#"],
        ]
    ]


def pretty_print(grid: list[list]):
    print(pretty_print(grid))


def pretty_string(grid: list[list]):
    return "\n".join(map(lambda row: "".join(map(lambda col: "." if col is None else col, row)), reversed(grid)))
