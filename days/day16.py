"""
Proboscidea Volcanium
"""
import re
from itertools import chain


class Valve(object):
    INPUT_PATTERN = re.compile("Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z\s,]+)")

    def __init__(self, raw_valve: str):
        match = Valve.INPUT_PATTERN.match(raw_valve.strip())
        id = match.group(1)
        flow_rate = int(match.group(2))
        connected_valve_ids = match.group(3).split(", ")
        self.id = id
        self.flow_rate = flow_rate
        self.connected_valve_ids = connected_valve_ids

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return "ID: {}".format(self.id)


class Actor(object):
    def __init__(self, current_valve: Valve, index: dict[str, Valve], opened_valves: set[Valve], time_remaining: int):
        self.current_valve = current_valve
        self.index = index
        self.opened_valves = opened_valves
        self.time_remaining = time_remaining

    def possible_future_states(self) -> set:
        states = set()
        if self.time_remaining == 0:
            return states
        new_time_remaining = self.time_remaining - 1
        if self.can_open():
            states.add(
                Actor(self.current_valve, self.index, set(chain(self.opened_valves, {self.current_valve})),
                      new_time_remaining))

        for next_valve in self.valves_can_move_to():
            states.add(Actor(next_valve, self.index, self.opened_valves, new_time_remaining))
        return states

    def can_open(self):
        return self.current_valve not in self.opened_valves and self.current_valve.flow_rate > 0

    def valves_can_move_to(self):
        return [self.index[valve_id] for valve_id in self.current_valve.connected_valve_ids]

    def pressure_released(self):
        total = 0
        for valve in self.opened_valves:
            total += self.index[valve.id].flow_rate
        return total

    def memo_key(self):
        return frozenset([self.current_valve.id, frozenset(self.opened_valves), self.time_remaining])


def parse_valves(raw_valves_and_pressure: list[str]) -> list[Valve]:
    return list(map(Valve, raw_valves_and_pressure))


def take_turn(actor: Actor, memo: dict):
    if actor.memo_key() in memo:
        return memo[actor.memo_key()]

    max_value = 0
    for future_actor in actor.possible_future_states():
        actor_score = future_actor.pressure_released()
        max_value = max(actor_score + take_turn(future_actor, memo), max_value)
    memo[actor.memo_key()] = max_value
    return max_value


def part_1(raw_valves_and_pressure: list[str]) -> str:
    valves = parse_valves(raw_valves_and_pressure)
    head = next(iter(filter(lambda v: v.id == "AA", valves)))
    memo = {}
    state = set()
    actor = Actor(head, {valve.id: valve for valve in valves}, state, 29)
    value = take_turn(actor, memo)
    return str(value)


def part_2(raw_valves_and_pressure: list[str]) -> str:
    valves = parse_valves(raw_valves_and_pressure)
    head = next(iter(filter(lambda v: v.id == "AA", valves)))
    return ""
