"""
Monkey in the Middle
"""
from functools import reduce
from typing import Iterable
from operator import add, mul, mod

from day3 import chunk
import re


class MonkeyVersion(object):
    def __init__(self, version: int):
        self.version = version


class MonkeyVersions(object):
    VERSION_1 = MonkeyVersion(1)
    VERSION_2 = MonkeyVersion(2)


class Monkey(object):
    ID_PATTERN = re.compile("Monkey ([0-9]):")
    STARTING_ITEMS_PATTERN = re.compile("Starting items: ([0-9\\s,]+)")
    OPERATION_PATTERN = re.compile("Operation: new = (old|[0-9]+) ([*+]) (old|[0-9]+)")
    TEST_PATTERN = re.compile("Test: divisible by ([0-9]+)")
    EVAL_PATTERN = re.compile("If (true|false): throw to monkey ([0-9]+)")

    def __init__(self, raw_monkey: Iterable[str]):
        iterable = iter(raw_monkey)

        raw_id = next(iterable)
        self.id = int(Monkey.ID_PATTERN.match(raw_id).group(1))

        raw_starting_items = next(iterable)
        self.items = list(
            map(lambda s: int(s), Monkey.STARTING_ITEMS_PATTERN.match(raw_starting_items).group(1).split(", ")))

        raw_operation = next(iterable)
        match = Monkey.OPERATION_PATTERN.match(raw_operation)
        lhs = match.group(1)
        operator = mul if match.group(2) == "*" else add
        rhs = match.group(3)
        self.operator = operator

        def operation(a: int) -> int:
            if lhs == rhs:
                return operator(a, a)
            else:
                return operator(a, int(rhs))

        self.operation = operation

        raw_test = next(iterable)
        divisor = int(Monkey.TEST_PATTERN.match(raw_test).group(1))
        self.divisor = divisor
        self.test = lambda a: mod(a, divisor) == 0

        raw_true_condition = next(iterable)
        self.true_monkey = int(Monkey.EVAL_PATTERN.match(raw_true_condition).group(2))

        raw_false_condition = next(iterable)
        self.false_monkey = int(Monkey.EVAL_PATTERN.match(raw_false_condition).group(2))

        self.inspections = 0

    def take_turn(self, monkey_index, version: MonkeyVersion) -> None:
        for i in range(len(self.items)):
            item = self.operation(self.items.pop(0))
            if version == MonkeyVersions.VERSION_1:
                reduced = item // 3
            else:
                # a mod n is true if a mod m * n is true
                all_divisors = reduce(lambda a, b: a * b, [monkey.divisor for monkey in monkey_index.values()])
                reduced = item % all_divisors
            monkey = self.true_monkey if self.test(reduced) else self.false_monkey
            monkey_index[monkey].items.append(reduced)
            self.inspections += 1

    def __repr__(self):
        return " | ".join([self.items.__repr__(), str(self.inspections), self.operator.__repr__()])


class RoundEvaluator(object):
    def __init__(self, monkeys: list[Monkey], num_rounds: int):
        self.monkeys = monkeys
        self.monkey_index = {monkey.id: monkey for monkey in monkeys}
        self.num_rounds = num_rounds

    def pass_rounds(self, version: MonkeyVersion = MonkeyVersions.VERSION_1) -> None:
        for _ in range(self.num_rounds):
            for monkey in self.monkeys:
                monkey.take_turn(self.monkey_index, version)


def part_1(raw_monkey_input: list[str]) -> str:
    monkeys = parse_monkey_input(raw_monkey_input)
    round_evaluator = RoundEvaluator(monkeys, 20)
    round_evaluator.pass_rounds()
    sorted_by_inspections = sorted(map(lambda m: m.inspections, monkeys), reverse=True)
    return str(sorted_by_inspections[0] * sorted_by_inspections[1])


def part_2(raw_monkey_input: list[str]) -> str:
    monkeys = parse_monkey_input(raw_monkey_input)
    round_evaluator = RoundEvaluator(monkeys, 10000)
    round_evaluator.pass_rounds(MonkeyVersions.VERSION_2)
    sorted_by_inspections = sorted(map(lambda m: m.inspections, monkeys), reverse=True)
    return str(sorted_by_inspections[0] * sorted_by_inspections[1])


def parse_monkey_input(raw_monkey_input: list[str]) -> list[Monkey]:
    monkey_instruction_length = 6
    chunked = chunk(list(filter(lambda s: s != "", map(lambda s: s.strip(), raw_monkey_input))),
                    monkey_instruction_length)
    return list(map(Monkey, chunked))
