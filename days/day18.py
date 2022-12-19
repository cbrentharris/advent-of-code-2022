"""
Boiling Boulders
"""


class ObsidianPixel(object):
    def __init__(self, raw_point: str):
        x, y, z = raw_point.strip().split(",")
        self.point = int(x), int(y), int(z)

    def __repr__(self):
        return self.point.__repr__()

    def __str__(self):
        return self.point.__str__()

    def sides_uncovered(self, pixels: set):
        x, y, z = self.point
        total_uncovered = 0
        for i in range(-1, 2, 2):
            with_x_offset = x + i, y, z
            with_y_offset = x, y + i, z
            with_z_offset = x, y, z + i
            for offset in [with_x_offset, with_y_offset, with_z_offset]:
                if offset not in pixels:
                    total_uncovered += 1
        return total_uncovered


def part_1(raw_obsidian_pixels: list[str]) -> str:
    obsidian_pixels = list(map(ObsidianPixel, raw_obsidian_pixels))
    pixel_set = set(map(lambda p: p.point, obsidian_pixels))
    return str(sum(map(lambda p: p.sides_uncovered(pixel_set), obsidian_pixels)))


def part_2(input: list[str]) -> str:
    return ""
