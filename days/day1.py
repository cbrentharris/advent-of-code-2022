import heapq

"""
Calorie Counting
"""


def part_1(input: list[str]) -> str:
    total = 0
    max_total = 0
    for line in stripped(input):
        if len(line) == 0:
            max_total = max(total, max_total)
            total = 0
        else:
            total += int(line)
    max_total = max(total, max_total)
    return str(max_total)


def part_2(input: list[str]) -> str:
    heap = []
    running_total = 0
    for line in stripped(input):
        if len(line) == 0:
            push_max(heap, running_total)
            running_total = 0
        else:
            running_total += int(line)
    if running_total != 0:
        push_max(heap, running_total)
    top_n = 3
    return str(sum(map(lambda x: pop_max(heap), range(top_n))))


def stripped(input: list[str]) -> list[str]:
    return list(map(lambda s: s.strip(), input))


def push_max(heap: list[(int, int)], val: int) -> None:
    heapq.heappush(heap, (-val, val))


def pop_max(heap: list[(int, int)]) -> int:
    return heapq.heappop(heap)[1]
