"""
Proboscidea Volcanium
"""
import sys
import heapq
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

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return "ID: {}".format(self.id)

    def __lt__(self, other):
        return self.id < other.id

    def init_paths(self, index):
        dist, prev = djikstras(self, index)
        self.dist = dist
        self.prev = prev


class Actor(object):
    def __init__(self, current_valve: Valve,
                 all_valves: frozenset[Valve],
                 index: dict[str, Valve],
                 my_opened_valves: frozenset[Valve],
                 time_remaining: int,
                 partner_opened_valves: frozenset[Valve]):
        self.current_valve = current_valve
        self.index = index
        self.my_opened_valves = my_opened_valves
        self.all_opened_valves = frozenset(chain(my_opened_valves, partner_opened_valves))
        self.partner_opened_valves = partner_opened_valves
        self.time_remaining = time_remaining
        self.all_valves = all_valves
        self.desirable_valves = all_valves - (self.all_opened_valves | {self.current_valve})

    def possible_future_states(self) -> frozenset:
        states = set()
        if self.time_remaining <= 0:
            return frozenset()

        for distance, next_valve in self.valves_should_move_to():
            states.add(
                Actor(next_valve, self.all_valves, self.index, frozenset(chain(self.my_opened_valves, {next_valve})),
                      self.time_remaining - distance - 1,
                      self.partner_opened_valves
                      ))
        return frozenset(states)

    def can_open(self):
        return self.current_valve not in self.all_opened_valves and self.current_valve.flow_rate > 0

    def is_open(self):
        return self.current_valve in self.all_opened_valves

    def valves_should_move_to(self):
        for valve in self.desirable_valves:
            distance_to_get_to = self.current_valve.dist[valve]
            if self.time_remaining - distance_to_get_to >= 1:
                yield distance_to_get_to, valve

    def pressure_released(self):
        return self.current_valve.flow_rate * self.time_remaining

    def primary_memo_key(self):
        return self.current_valve.id, self.all_opened_valves, self.time_remaining

    def secondary_memo_key(self):
        return self.current_valve.id, self.time_remaining

    def clone(self, other):
        return Actor(self.current_valve, self.all_valves, self.index, self.my_opened_valves,
                     self.time_remaining,
                     other.my_opened_valves)

    def __hash__(self):
        return hash(self.primary_memo_key())

    def __eq__(self, other):
        return self.primary_memo_key() == other.primary_memo_key()

    def __repr__(self):
        return "{}, {}, {}".format(self.current_valve.id, self.all_opened_valves, self.time_remaining)


def parse_valves(raw_valves_and_pressure: list[str]) -> list[Valve]:
    return list(map(Valve, raw_valves_and_pressure))


def take_turn(actor: Actor, memo: dict):
    if actor.primary_memo_key() in memo:
        return memo[actor.primary_memo_key()]
    max_value = 0
    for future_actor in actor.possible_future_states():
        actor_score = future_actor.pressure_released()
        max_value = max(actor_score + take_turn(future_actor, memo), max_value)
    memo[actor.primary_memo_key()] = max_value
    return max_value


def take_turn_parallelized(first: Actor, second: Actor, memo: dict):
    full_memo_key = frozenset([first.secondary_memo_key(), second.secondary_memo_key(), first.all_opened_valves])
    if full_memo_key in memo:
        return memo[full_memo_key]

    max_value = 0
    first_possible_future_states = first.possible_future_states()
    for first_future_state in first_possible_future_states:
        first_actor_score = first_future_state.pressure_released()
        second_possible_future_states = second.clone(first_future_state).possible_future_states()
        for second_future_state in second_possible_future_states:
            second_actor_score = second_future_state.pressure_released()
            max_value = max(first_actor_score + second_actor_score + take_turn_parallelized(
                first_future_state.clone(second_future_state),
                second_future_state,
                memo), max_value)
    memo[full_memo_key] = max_value
    return max_value


def part_1(raw_valves_and_pressure: list[str]) -> str:
    valves = parse_valves(raw_valves_and_pressure)
    desirable_valves = frozenset([v for v in valves if v.flow_rate > 0])
    index = {valve.id: valve for valve in valves}
    for valve in valves:
        valve.init_paths(index)
    head = next(iter(filter(lambda v: v.id == "AA", valves)))
    memo = {}
    actorv2 = Actor(head, desirable_valves, index, frozenset(), 30, frozenset())
    value = take_turn(actorv2, memo)
    print(len(memo))
    return str(value)


def part_2(raw_valves_and_pressure: list[str]) -> str:
    valves = parse_valves(raw_valves_and_pressure)
    desirable_valves = frozenset([v for v in valves if v.flow_rate > 0])
    index = {valve.id: valve for valve in valves}
    for valve in valves:
        valve.init_paths(index)
    head = next(iter(filter(lambda v: v.id == "AA", valves)))
    memo = {}
    multi_actor_penalty = 4
    firstv2 = Actor(head, desirable_valves, index, frozenset(),
                    30 - multi_actor_penalty, frozenset())
    secondv2 = Actor(head, desirable_valves, index, frozenset(),
                     30 - multi_actor_penalty, frozenset())
    value = take_turn_parallelized(firstv2, secondv2, memo)
    print(len(memo))
    return str(value)


def djikstras(start: Valve, index: dict[str, Valve]):
    nodes_to_process = []
    dist = {}
    prev = {}

    for k, v in index.items():
        if v == start:
            dist[v] = 0
            heapq.heappush(nodes_to_process, (dist[v], v))
        else:
            dist[v] = sys.maxsize
            prev[v] = None

    while len(nodes_to_process) > 0:
        node_to_process = heapq.heappop(nodes_to_process)[1]
        for valve_id in node_to_process.connected_valve_ids:
            val = dist[node_to_process] + 1
            neighbor = index[valve_id]
            if val < dist[neighbor]:
                dist[neighbor] = val
                prev[neighbor] = node_to_process
                heapq.heappush(nodes_to_process, (dist[neighbor], neighbor))

    return dist, prev
