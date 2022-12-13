from typing import Iterable


def chain_functions(i, *functions):
    result = i
    for f in functions:
        result = f(result)
    return result


def chunk(l: list, n: int) -> Iterable[Iterable]:
    for i in range(0, len(l), n):
        yield l[i:i + n]
