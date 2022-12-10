"""
Cathode-Ray Tube
"""


class CPUInstruction(object):
    NOOP = "noop"
    ADD = "add"

    def __init__(self, raw_instruction: str, registers: dict):
        self.registers = registers
        cleaned = raw_instruction.strip()
        if cleaned == CPUInstruction.NOOP:
            self.cycles = 1
            self.instruction = cleaned
        else:
            instruction_and_register, value = cleaned.split(" ")
            self.instruction = CPUInstruction.ADD
            self.register = instruction_and_register.lstrip(CPUInstruction.ADD)
            self.value = int(value)
            self.cycles = 2

    def evaluate(self) -> None:
        if self.instruction == CPUInstruction.NOOP:
            pass
        else:
            register_value = self.registers[self.register]
            register_value = register_value + self.value
            self.registers[self.register] = register_value

    def __repr__(self):
        if self.instruction == CPUInstruction.NOOP:
            return self.instruction
        return self.instruction + " " + self.register + " " + str(self.value)


class CPU(object):

    def __init__(self, cpu_instructions: list[CPUInstruction], registers: dict):
        self.registers = registers
        self.cpu_instructions = cpu_instructions
        self.sample_interval = 40
        self.sample_counter = 20
        self.instruction_counter = 0
        self.current_instruction = cpu_instructions.pop(0)

    def sample(self, register):
        for _ in range(self.sample_counter):
            self.advance_cycle()
        self.sample_counter = self.sample_interval
        return self.registers[register]

    def advance_cycle(self):
        if self.current_instruction.cycles == 0:
            self.current_instruction.evaluate()
            self.current_instruction = self.cpu_instructions.pop(0)
        self.current_instruction.cycles -= 1
        self.instruction_counter += 1


class CRT(object):
    def __init__(self, cpu: CPU, sprite_register: str, width: int, height: int):
        self.cpu = cpu
        self.sprite_width = 3
        self.sprite_register = sprite_register
        self.screen_width = width
        self.screen_height = height

    def sprite_location(self) -> int:
        return self.cpu.registers[self.sprite_register]

    @staticmethod
    def overlaps(sprite_location: int, pixel_location: int):
        return abs(sprite_location - pixel_location) <= 1

    def get_display_character(self, column: int) -> str:
        if self.overlaps(self.sprite_location(), column):
            return '#'
        return '.'

    def render(self) -> str:
        pixels = [[] for _ in range(self.screen_height)]
        for row in range(self.screen_height):
            for column in range(self.screen_width):
                self.cpu.advance_cycle()
                pixels[row].append(self.get_display_character(column))

        return "\n".join(["".join(row) for row in pixels])


def part_1(instructions: list[str]) -> str:
    register = 'x'
    registers = {register: 1}
    cpu_instructions = list(map(lambda i: CPUInstruction(i, registers), instructions))
    cpu = CPU(cpu_instructions, registers)
    sample_count = 6
    scores = [cpu.sample(register) * cpu.instruction_counter for _ in range(sample_count)]
    return str(sum(scores))


def part_2(instructions: list[str]) -> str:
    register = 'x'
    registers = {register: 1}
    cpu_instructions = list(map(lambda i: CPUInstruction(i, registers), instructions))
    cpu = CPU(cpu_instructions, registers)
    crt = CRT(cpu, register, 40, 6)
    return crt.render()
