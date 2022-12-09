from typing import Iterable, Callable

"""
Treetop Tree House
"""


def parse_tree_rows(tree_grid: list[str]) -> list[list[int]]:
    return list(map(lambda row: list(map(int, list(row.strip()))), tree_grid))


def part_1(tree_grid: list[str]) -> str:
    tree_matrix = parse_tree_rows(tree_grid)
    columns = len(tree_matrix[0])
    rows = len(tree_matrix)
    edge_count = rows * 2 + (columns - 2) * 2

    visible_set = set()

    for row in range(1, rows - 1):
        left_max = tree_matrix[row][0]
        for column in range(1, columns - 1):
            element = tree_matrix[row][column]
            if element > left_max:
                visible_set.add(((row, column), element))
            left_max = max(left_max, element)

    for row in range(1, columns - 1):
        right_max = tree_matrix[row][rows - 1]
        for column in range(rows - 2, 0, -1):
            element = tree_matrix[row][column]
            if element > right_max:
                visible_set.add(((row, column), element))
            right_max = max(right_max, element)

    for column in range(1, rows - 1):
        down_max = tree_matrix[0][column]
        for row in range(1, columns - 1):
            element = tree_matrix[row][column]
            if element > down_max:
                visible_set.add(((row, column), element))
            down_max = max(down_max, element)

    for column in range(1, columns - 1):
        up_max = tree_matrix[rows - 1][column]
        for row in range(columns - 2, 0, -1):
            element = tree_matrix[row][column]
            if element > up_max:
                visible_set.add(((row, column), element))
            up_max = max(up_max, element)

    return str(edge_count + len(visible_set))


def part_2(tree_grid: list[str]) -> str:
    tree_matrix = parse_tree_rows(tree_grid)
    columns = len(tree_matrix[0])
    rows = len(tree_matrix)

    def scenic_score(row: int, col: int) -> int:
        element = tree_matrix[row][col]

        left_visibles = find_visible_trees(element, decrementer(col), lambda x: tree_matrix[row][x])
        right_visibles = find_visible_trees(element, incrementer(col, columns), lambda x: tree_matrix[row][x])
        down_visibles = find_visible_trees(element, incrementer(row, rows), lambda x: tree_matrix[x][col])
        up_visibles = find_visible_trees(element, decrementer(row), lambda x: tree_matrix[x][col])

        return left_visibles * right_visibles * up_visibles * down_visibles

    rows_and_columns = [(row, col) for row in range(1, rows - 1) for col in range(1, columns - 1)]
    return str(max(map(lambda args: scenic_score(*args), rows_and_columns)))


def find_visible_trees(element: int, index_iterator: range, value_getter: Callable[[int], int]) -> int:
    visibles = 0
    max_so_far = -1
    for i in index_iterator:
        value = value_getter(i)
        visibles += 1

        if value >= element:
            break

        max_so_far = max(max_so_far, value)

    return visibles


def decrementer(val: int) -> range:
    return range(val - 1, -1, -1)


def incrementer(val: int, end: int) -> range:
    return range(val + 1, end)
