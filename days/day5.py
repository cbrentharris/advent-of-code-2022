"""
Supply Stacks
"""
from typing import Iterable, Callable


class Instruction(object):
    def __init__(self, s):
        tokenized = s.split(" ")
        self.quantity_to_move = int(tokenized[1])
        self.source = int(tokenized[3])
        self.sink = int(tokenized[5])


def to_stacks(stack_data: list[str]) -> list[list]:
    num_stacks = int(stack_data.pop().strip()[-1])
    stacks = [[] for _ in range(num_stacks)]
    stack_data.reverse()
    for stack_string in stack_data:
        for i in range(num_stacks):
            value_start = i * 3 + i
            value_end = value_start + 3
            value = stack_string[value_start:value_end]
            if value == "   ":
                pass
            else:
                stacks[i].append(value.strip("[]"))
    return stacks


def to_instructions(instruction_data: list[str]) -> Iterable[Instruction]:
    return map(Instruction, instruction_data)


def follow_instruction(instruction: Instruction, stacks: list[list]) -> None:
    source_stack = stacks[instruction.source - 1]
    sink_stack = stacks[instruction.sink - 1]
    sink_stack.extend([source_stack.pop() for _ in range(instruction.quantity_to_move)])


def follow_advanced_instruction(instruction: Instruction, stacks: list[list]) -> None:
    source_stack = stacks[instruction.source - 1]
    sink_stack = stacks[instruction.sink - 1]
    stacks[instruction.source - 1] = source_stack[:len(source_stack) - instruction.quantity_to_move]
    sink_stack.extend(source_stack[len(source_stack) - instruction.quantity_to_move:len(source_stack)])


def part_1(stack_input: list[str]) -> str:
    return evaluate_with_instructions(stack_input, follow_instruction)


def part_2(stack_input: list[str]) -> str:
    return evaluate_with_instructions(stack_input, follow_advanced_instruction)


def evaluate_with_instructions(stack_input: list[str],
                               instruction_follower: Callable[[Instruction, list[list]], None]) -> str:
    cleaned_input = list(map(lambda x: x.strip(), stack_input))
    partition_index = cleaned_input.index("")
    stack_data = stack_input[:partition_index]
    instruction_data = stack_input[partition_index + 1:]
    stacks = to_stacks(stack_data)
    instructions = to_instructions(instruction_data)
    for instruction in instructions:
        instruction_follower(instruction, stacks)
    return "".join(map(lambda stack: stack.pop(), stacks))
