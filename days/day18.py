"""
Boiling Boulders
"""
from functools import reduce
from typing import Tuple, Iterable


def surrounding_pixels(point: [int, int, int]) -> Iterable[Tuple[int, int, int]]:
    x, y, z = point
    for i in range(-1, 2, 2):
        yield x + i, y, z
        yield x, y + i, z
        yield x, y, z + i


def will_be_surrounded(pixel: [int, int, int], pixels: set[int, int, int]) -> bool:
    x, y, z = pixel
    zs_in_direction = set(map(lambda p: p[2], filter(lambda p: p[0] == x and p[1] == y, pixels)))
    if len(zs_in_direction) == 0:
        return False
    max_z = max(zs_in_direction)
    min_z = min(zs_in_direction)
    ys_in_direction = set(map(lambda p: p[1], filter(lambda p: p[0] == x and p[2] == z, pixels)))
    if len(ys_in_direction) == 0:
        return False

    max_y = max(ys_in_direction)
    min_y = min(ys_in_direction)
    xs_in_direction = set(map(lambda p: p[0], filter(lambda p: p[1] == y and p[2] == z, pixels)))
    if len(xs_in_direction) == 0:
        return False
    max_x = max(xs_in_direction)
    min_x = min(xs_in_direction)
    return min_x < x < max_x and min_y < y < max_y and min_z < z < max_z


def sides_uncovered(point: [int, int, int], pixels: set) -> int:
    total_uncovered = 0
    for point in surrounding_pixels(point):
        if point not in pixels:
            total_uncovered += 1
    return total_uncovered


def sides_covered(point: [int, int, int], pixels: set) -> int:
    total_covered = 0
    for point in surrounding_pixels(point):
        if point in pixels:
            total_covered += 1
    return total_covered


def leads_to_the_outside(point: [int, int, int], pixels: set[[int, int, int]]) -> bool:
    for p in surrounding_pixels(point):
        if p not in pixels:
            if not will_be_surrounded(p, pixels):
                return True
    return False


def air_pockets(point: [int, int, int], pixels: set[[int, int, int]]) -> set[[int, int, int]]:
    pockets = set()
    for point in surrounding_pixels(point):
        if point not in pixels and not leads_to_the_outside(point, pixels):
            pockets.add(point)
    return pockets


def parse(raw_point: str) -> [int, int, int]:
    x, y, z = raw_point.strip().split(",")
    return int(x), int(y), int(z)


def part_1(raw_obsidian_pixels: list[str]) -> str:
    obsidian_pixels = set(map(parse, raw_obsidian_pixels))
    return str(surface_area(obsidian_pixels))


def part_2(raw_obsidian_pixels: list[str]) -> str:
    obsidian_pixels = set(map(parse, raw_obsidian_pixels))
    area = surface_area(obsidian_pixels)
    return str(area - air_pocket_area(obsidian_pixels))


def surface_area(obsidian_pixels: set[[int, int, int]]) -> int:
    return sum(map(lambda p: sides_uncovered(p, obsidian_pixels), obsidian_pixels))


def air_pocket_area(obsidian_pixels: set[[int, int, int]]) -> int:
    pockets = reduce(set.union, map(lambda p: air_pockets(p, obsidian_pixels), obsidian_pixels))
    return sum(map(lambda p: sides_covered(p, obsidian_pixels), pockets))
