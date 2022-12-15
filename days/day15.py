"""
Beacon Exclusion Zone
"""
import re
from typing import Union

from coordinate_tools import manhattan_distance


class BoundsAlongRow(object):
    def __init__(self, left_bound, right_bound, y):
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.y = y

    def can_merge(self, other) -> bool:
        return self.left_bound <= other.left_bound <= self.right_bound

    def merge(self, other):
        if not self.can_merge(other):
            raise Exception("Cannot merge : {first} with {second}".format(first=self, second=other))
        self.left_bound = min(self.left_bound, other.left_bound)
        self.right_bound = max(self.right_bound, other.right_bound)
        return self

    def __lt__(self, other):
        if self.left_bound == other.left_bound:
            return self.right_bound < other.right_bound
        return self.left_bound < other.left_bound

    def row_length(self):
        return self.right_bound - self.left_bound

    def __repr__(self):
        return "Left: {}, Right: {}".format(self.left_bound, self.right_bound)


class Sensor(object):
    INTEGER_PATTERN = re.compile("-?\d+")

    def __init__(self, raw_sensor_and_beacon):
        all_integers = map(int, Sensor.INTEGER_PATTERN.findall(raw_sensor_and_beacon))

        sensor_x, sensor_y, beacon_x, beacon_y = all_integers
        self.position = (sensor_x, sensor_y)
        self.closest_beacon = (beacon_x, beacon_y)

    def __repr__(self):
        return "Position={position}, Closest Beacon={closest_beacon}".format(position=self.position,
                                                                             closest_beacon=self.closest_beacon)

    def bounds_with_no_beacons(self, target_y) -> Union[None, BoundsAlongRow]:
        distance = manhattan_distance(self.position, self.closest_beacon)
        x, y = self.position
        y_delta = abs(y - target_y)
        if y_delta > distance:
            return None
        possible_x_delta = distance - y_delta
        return BoundsAlongRow(x - possible_x_delta, x + possible_x_delta, y)

    def bounds_with_no_beacons_search(self, target_y, lower_bound, upper_bound) -> Union[None, BoundsAlongRow]:
        distance = manhattan_distance(self.position, self.closest_beacon)
        x, y = self.position
        y_delta = abs(y - target_y)
        if any([y_delta > distance, lower_bound > target_y, upper_bound < target_y]):
            return None
        possible_x_delta = distance - abs(target_y - y)
        min_x = max(lower_bound, x - possible_x_delta)
        max_x = min(upper_bound, x + possible_x_delta)
        if min_x > max_x:
            return None
        return BoundsAlongRow(min_x, max_x, target_y)


"""
In this algorithm, we materialized bounds along an axis
"""


def part_1(raw_sensors_and_beacons: list[str], y_position: int) -> str:
    sensors = map(Sensor, raw_sensors_and_beacons)
    bounds = [sensor.bounds_with_no_beacons(y_position) for sensor in sensors if
              sensor.bounds_with_no_beacons(y_position)
              is not None]
    merged_bounds = merge(bounds)
    return str(sum(map(lambda bound: bound.row_length(), merged_bounds)))


def find_beacon_position(merged_bounds, lower_bound):
    i = lower_bound
    while len(merged_bounds) > 0:
        bound = merged_bounds.pop(0)
        if bound.left_bound <= i <= bound.right_bound:
            i = bound.right_bound + 1
    return i


def tuning_frequency(beacon_x_position, beacon_y_position):
    return beacon_x_position * 4000000 + beacon_y_position


def part_2(raw_sensors_and_beacons: list[str], lower_bound: int, upper_bound: int) -> str:
    sensors = list(map(Sensor, raw_sensors_and_beacons))
    for beacon_y_position in range(lower_bound, upper_bound + 1):
        bounds = list(filter(lambda x: x is not None, [sensor.bounds_with_no_beacons_search(beacon_y_position,
                                                                                            lower_bound, upper_bound)
                                                       for
                                                       sensor in sensors]))
        merged_bounds = merge(bounds)
        row_count = sum_count(merged_bounds)
        if row_count < upper_bound:
            beacon_x_position = find_beacon_position(merged_bounds, lower_bound)
            return str(tuning_frequency(beacon_x_position, beacon_y_position))

    raise Exception("Should have found a tuning frequency")


def merge(bounds: list[BoundsAlongRow]) -> list[BoundsAlongRow]:
    sorted_bounds = list(sorted(bounds))
    current_bound = sorted_bounds.pop(0)
    merged_bounds = []
    while len(sorted_bounds) > 0:
        next_bound = sorted_bounds.pop(0)
        if current_bound.can_merge(next_bound):
            current_bound = current_bound.merge(next_bound)
        else:
            merged_bounds.append(current_bound)
            current_bound = next_bound
    merged_bounds.append(current_bound)
    return merged_bounds


def sum_count(merged_bounds: list[BoundsAlongRow]) -> int:
    return sum(map(lambda bound: bound.row_length(), merged_bounds))
