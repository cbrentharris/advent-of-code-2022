def manhattan_distance(a: [int, int], b: [int, int]) -> int:
    a_x, a_y = a
    b_x, b_y = b
    return abs(a_x - b_x) + abs(a_y - b_y)
