"""
Monkey Math
"""
import re
from operator import add, sub, mul, truediv


class Monkey(object):
    OPS = {
        "-": sub,
        "*": mul,
        "/": truediv,
        "+": add,
    }
    INVERSES = {
        "-": add,
        "*": truediv,
        "+": sub,
        "/": mul
    }
    OP_REGEX = re.compile(r"([a-z]{4}): ([a-z]{4}) (\+|\-|\*|/) ([a-z]{4})")
    SINK_REGEX = re.compile(r"([a-z]{4}): ([0-9]+)")

    def __init__(self, raw_str: str):
        raw_str = raw_str.strip()
        match = Monkey.SINK_REGEX.match(raw_str)
        self.value = None
        self.lhs = None
        self.op = None
        self.rhs = None
        if match is not None:
            self.id = match.group(1)
            self.value = int(match.group(2))

        else:
            match = Monkey.OP_REGEX.match(raw_str)
            self.id = match.group(1)
            self.lhs = match.group(2)
            self.op = match.group(3)
            self.rhs = match.group(4)

    def __str__(self):
        return "ID: {}, Value: {}, LHS: {}, OP: {}, RHS: {}".format(self.id, self.value, self.lhs, self.op, self.rhs)

    def __repr__(self):
        return self.__str__()

    def evaluate(self, monkey_index: dict):
        if self.value is not None:
            return self.value

        lhs_monkey = monkey_index[self.lhs].evaluate(monkey_index)
        rhs_monkey = monkey_index[self.rhs].evaluate(monkey_index)
        return Monkey.OPS[self.op](lhs_monkey, rhs_monkey)

    def find_human_val(self, monkey_index: dict):
        lhs_monkey = monkey_index[self.lhs]
        rhs_monkey = monkey_index[self.rhs]
        lhs_has_human = lhs_monkey.has_human(monkey_index)
        lhs_value = lhs_monkey.evaluate(monkey_index)
        rhs_value = rhs_monkey.evaluate(monkey_index)
        if lhs_has_human:
            return lhs_monkey.correct_value(rhs_value, monkey_index)
        else:
            return rhs_monkey.correct_value(lhs_value, monkey_index)

    def correct_value(self, answer, monkey_index):
        if self.id == "humn":
            return answer
        lhs_monkey = monkey_index[self.lhs]
        rhs_monkey = monkey_index[self.rhs]

        lhs_has_human = lhs_monkey.has_human(monkey_index)
        lhs_value = lhs_monkey.evaluate(monkey_index)
        rhs_value = rhs_monkey.evaluate(monkey_index)
        if lhs_has_human:
            corrected_value = Monkey.INVERSES[self.op](answer, rhs_value)
            return lhs_monkey.correct_value(corrected_value, monkey_index)
        else:
            if self.op == "-":
                corrected_value = Monkey.OPS[self.op](lhs_value, answer)
            else:
                corrected_value = Monkey.INVERSES[self.op](answer, lhs_value)
            return rhs_monkey.correct_value(corrected_value, monkey_index)

    def has_human(self, monkey_dict: dict):
        if self.value is not None:
            return self.id == "humn"
        if self.lhs == "humn" or self.rhs == "humn":
            return True
        return monkey_dict[self.lhs].has_human(monkey_dict) or monkey_dict[self.rhs].has_human(monkey_dict)


def part_1(raw_monkeys: list[str]) -> str:
    monkeys = {monkey.id: monkey for monkey in map(Monkey, raw_monkeys)}
    root_monkey = monkeys["root"]
    return str(root_monkey.evaluate(monkeys))


def part_2(raw_monkeys: list[str]) -> str:
    monkeys = {monkey.id: monkey for monkey in map(Monkey, raw_monkeys)}
    root_monkey = monkeys["root"]
    return str(root_monkey.find_human_val(monkeys))
