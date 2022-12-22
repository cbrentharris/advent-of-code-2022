"""
Not Enough Minerals
"""
import copy
import re
from typing import Iterable, Tuple
import time


class BluePrint(object):
    INT_REGEX = r"([0-9]+)"

    def __init__(self, raw_blueprint: str):
        blueprint_id, ore_robot_ore_cost, clay_robot_ore_cost, obsidian_robot_ore_cost, obsidian_robot_clay_cost, geode_robot_ore_cost, geode_robot_obsidian_cost = list(
            map(int, re.findall(BluePrint.INT_REGEX, raw_blueprint)))
        self.blueprint_id = blueprint_id
        self.ore_robot_ore_cost = ore_robot_ore_cost
        self.clay_robot_ore_cost = clay_robot_ore_cost
        self.obsidian_robot_ore_cost = obsidian_robot_ore_cost
        self.obsidian_robot_clay_cost = obsidian_robot_clay_cost
        self.geode_robot_ore_cost = geode_robot_ore_cost
        self.geode_robot_obsidian_cost = geode_robot_obsidian_cost

    def __str__(self):
        return "ID: {}, Ore Robot Ore Cost: {}, Clay Robot Ore Cost: {}, Obsidian Robot Ore Cost: {}, Obsidian Robot Clay Cost: {}, Geode Robot Ore Cost: {}, Geode Robot Obsidian Cost: {}".format(
            self.blueprint_id,
            self.ore_robot_ore_cost,
            self.clay_robot_ore_cost,
            self.obsidian_robot_ore_cost,
            self.obsidian_robot_clay_cost,
            self.geode_robot_ore_cost,
            self.geode_robot_obsidian_cost
        )


class Scenario(object):
    def __init__(self, blueprint, time_remaining: int, ore_robots=0):
        self.ore_robots = ore_robots
        self.blueprint = blueprint
        self.time_remaining = time_remaining
        self.initial_time_remaining = time_remaining

        self.clay_robots = 0
        self.obsidian_robots = 0
        self.geode_robots = 0

        self.ore = 0
        self.clay = 0
        self.obsidian = 0
        self.geodes = 0

        self.parent = None

        self.pending_ore_robots = 0
        self.pending_geode_robots = 0
        self.pending_clay_robots = 0
        self.pending_obsidian_robots = 0

    def pass_time(self):
        self.time_remaining -= 1
        self.geode_robots += self.pending_geode_robots
        self.ore_robots += self.pending_ore_robots
        self.clay_robots += self.pending_clay_robots
        self.obsidian_robots += self.pending_obsidian_robots

        self.pending_geode_robots = 0
        self.pending_ore_robots = 0
        self.pending_clay_robots = 0
        self.pending_obsidian_robots = 0

    def collect(self):
        if self.time_remaining > 0:
            self.ore += self.ore_robots
            self.clay += self.clay_robots
            self.obsidian += self.obsidian_robots
            self.geodes += self.geode_robots

    def spend(self) -> Iterable:
        if self.can_increase_geode_rate():
            yield self.spend_on_geode()
        if self.can_increase_obsidian_rate():
            yield self.spend_on_obsidian()
        if self.can_increase_ore_rate():
            yield self.spend_on_ore()
        if self.can_increase_clay_rate():
            yield self.spend_on_clay()
        if not all([self.can_increase_geode_rate(), self.can_increase_ore_rate(), self.can_increase_obsidian_rate(),
                    self.can_increase_clay_rate()]):
            yield copy.copy(self)

    def can_increase_ore_rate(self):
        return self.ore >= self.blueprint.ore_robot_ore_cost

    def spend_on_ore(self):
        clone = copy.copy(self)
        clone.parent = self
        clone.pending_ore_robots += 1
        clone.ore -= clone.blueprint.ore_robot_ore_cost
        return clone

    def can_increase_clay_rate(self):
        return self.ore >= self.blueprint.clay_robot_ore_cost

    def spend_on_clay(self):
        clone = copy.copy(self)
        clone.parent = self
        clone.ore -= clone.blueprint.clay_robot_ore_cost
        clone.pending_clay_robots += 1
        return clone

    def can_increase_obsidian_rate(self):
        return self.ore >= self.blueprint.obsidian_robot_ore_cost and self.clay >= self.blueprint.obsidian_robot_clay_cost

    def spend_on_obsidian(self):
        clone = copy.copy(self)
        clone.parent = self
        clone.pending_obsidian_robots += 1
        clone.ore -= clone.blueprint.obsidian_robot_ore_cost
        clone.clay -= clone.blueprint.obsidian_robot_clay_cost
        return clone

    def can_increase_geode_rate(self):
        return self.obsidian >= self.blueprint.geode_robot_obsidian_cost and self.ore >= self.blueprint.geode_robot_ore_cost

    def spend_on_geode(self):
        clone = copy.copy(self)
        clone.parent = self
        clone.pending_geode_robots += 1
        clone.ore -= clone.blueprint.geode_robot_ore_cost
        clone.obsidian -= clone.blueprint.geode_robot_obsidian_cost
        return clone

    def __str__(self):
        return "Ore robots: {}, Clay robots: {}, Obsidian robots: {}, Geode robots: {}, Ore: {}, Clay: {}, Obsidian: {}, Geodes: {}, Time Remaining: {}, Time Elapsed: {}".format(
            self.ore_robots, self.clay_robots, self.obsidian_robots, self.geode_robots, self.ore, self.clay,
            self.obsidian, self.geodes, self.time_remaining, self.initial_time_remaining - self.time_remaining)

    def __hash__(self):
        return hash(self.memo_key())

    def __eq__(self, other):
        return self.memo_key() == other.memo_key()

    def memo_key(self):
        return (self.ore, self.clay, self.obsidian, self.geodes, self.ore_robots, self.clay_robots,
                self.obsidian_robots, self.geode_robots, self.time_remaining,
                self.pending_clay_robots,
                self.pending_obsidian_robots,
                self.pending_ore_robots,
                self.pending_geode_robots
                )

    def quality_score(self):
        return self.geodes * self.blueprint.blueprint_id

    def should_not_continue(self):
        return self.has_too_many_robots() or self.is_past_time()

    def has_too_many_robots(self):
        return self.clay_robots > self.blueprint.obsidian_robot_clay_cost or self.obsidian_robots > self.blueprint.geode_robot_obsidian_cost or self.ore_robots > max(
            self.blueprint.clay_robot_ore_cost, self.blueprint.obsidian_robot_ore_cost,
            self.blueprint.geode_robot_ore_cost)

    def is_past_time(self):
        return self.time_remaining < 0

    def max_possible_geodes(self):
        return self.geodes + self.geode_robots * self.time_remaining + self.time_remaining * (
                self.time_remaining + 1) / 2 * self.geode_robots_per_minute()

    def geode_robots_per_minute(self):
        ore_velocity = self.ore_robots
        obsidian_velocity = self.obsidian_robots
        ore_per_minute = ore_velocity / self.blueprint.geode_robot_ore_cost
        geode_per_minute = obsidian_velocity / self.blueprint.geode_robot_obsidian_cost
        return min(1, max(ore_per_minute, geode_per_minute))

    def eventual_geodes(self):
        return self.geodes + self.geode_robots * self.time_remaining


def maximum_geodes(scenario: Scenario, minimized_scenario: dict[Tuple, Scenario],
                   maximum_eventual_geodes: dict[int, int]) -> Scenario:
    memo_key = scenario.memo_key()

    if memo_key in minimized_scenario:
        return minimized_scenario[memo_key]

    local_max = scenario
    for sub_scenario in scenario.spend():
        sub_scenario.collect()
        sub_scenario.pass_time()
        if sub_scenario.should_not_continue():
            continue
        time_remaining = sub_scenario.time_remaining
        impossible_to_beat_another_scenario = maximum_eventual_geodes.get(time_remaining,
                                                                          -1) > sub_scenario.max_possible_geodes()
        if impossible_to_beat_another_scenario:
            continue
        local_max = max(local_max, maximum_geodes(sub_scenario, minimized_scenario, maximum_eventual_geodes),
                        key=lambda s: s.geodes)
        maximum_eventual_geodes[time_remaining] = max(maximum_eventual_geodes.get(time_remaining, -1),
                                                      sub_scenario.eventual_geodes())

    minimized_scenario[memo_key] = local_max
    return local_max


def part_1(raw_blueprints: list[str]) -> str:
    blueprints = list(map(BluePrint, raw_blueprints))
    score = 0
    scenarios_explored = 0
    start = time.time()
    for idx, blueprint in enumerate(blueprints):
        minimized_scenarios = {}
        scenario = maximum_geodes(Scenario(blueprint, 24, ore_robots=1), minimized_scenarios, {})
        score += scenario.quality_score()
        scenarios_explored += len(minimized_scenarios)
        print_progress(start, len(blueprints), idx, scenarios_explored, score)

    return str(score)


def part_2(raw_blueprints: list[str]) -> str:
    blueprints = list(map(BluePrint, raw_blueprints))
    score = 1
    scenarios_explored = 0
    start = time.time()
    subset_of_blueprints = blueprints[:3]
    for idx, blueprint in enumerate(subset_of_blueprints):
        minimized_scenarios = {}
        scenario = maximum_geodes(Scenario(blueprint, 32, ore_robots=1), minimized_scenarios, {})
        score *= scenario.geodes
        scenarios_explored += len(minimized_scenarios)
        print_progress(start, len(subset_of_blueprints), idx, scenarios_explored, score)

    return str(score)


def print_progress(start_time, total_blueprints_to_process, current_blueprint_index,
                   total_elements_processed, score):
    minutes_elapsed = (time.time() - start_time) / 60
    percent_finished = (current_blueprint_index + 1) / total_blueprints_to_process
    minutes_remaining = minutes_elapsed / (current_blueprint_index + 1) * (
            total_blueprints_to_process - (current_blueprint_index + 1))
    formatted = "Minutes Elapsed: {:.2f}. Estimated Minutes Remaining: {:.2f}. Percent Finished: {:.2f}. ({} / {}) Blueprints Done. Total Scenarios Explored: {}. Running Score: {}.\n".format(
        minutes_elapsed,
        minutes_remaining,
        percent_finished * 100,
        current_blueprint_index + 1,
        total_blueprints_to_process,
        total_elements_processed,
        score)
    print(formatted)
