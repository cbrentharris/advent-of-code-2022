"""
Distress Signal
"""
import json
from functools import reduce
from itertools import chain
from operator import mul
from typing import Iterable, Union

from days.local_functools import chain_functions, chunk


class Packet(object):
    def __init__(self, items: list):
        self.items = items

    def __lt__(self, other):
        return self.less_than(self.items, other.items)

    def less_than(self, left: Union[list, int], right: Union[list, int]) -> Union[None, bool]:
        if type(left) == type(right) == int:
            if left == right:
                return None
            return left < right
        if type(left) == type(right) == list:
            for result in map(lambda index: self.less_than(left[index], right[index]),
                              range(min(len(left), len(right)))):
                if result is None:
                    continue
                return result
            if len(left) == len(right):
                return None
            return len(left) < len(right)
        else:
            if type(left) == int:
                return self.less_than([left], right)
            else:
                return self.less_than(left, [right])


def to_packets(raw_packets: Iterable[str]) -> Iterable[Packet]:
    return chain_functions(
        raw_packets,
        lambda packets: map(lambda packet: packet.strip(), packets),
        lambda packets: filter(lambda packet: packet != "", packets),
        lambda packets: map(json.loads, packets),
        lambda packets: map(Packet, packets)
    )


def part_1(raw_pairs_of_packets: list[str]) -> str:
    def chunk_into_twos(packets: Iterable[Packet]) -> Iterable[Iterable[Packet]]:
        return chunk(list(packets), 2)

    def in_the_right_order(chunked_packets: Iterable[Iterable[Packet]]) -> Iterable[bool]:
        def compare(packets: Iterable[Packet]) -> [bool, list[Packet]]:
            packet_list = list(packets)
            return packet_list[0].__lt__(packet_list[1])

        return map(compare, chunked_packets)

    return chain_functions(
        raw_pairs_of_packets,
        to_packets,
        chunk_into_twos,
        in_the_right_order,
        list,
        enumerate,
        lambda packet_pairs: filter(lambda packet_pair: packet_pair[1], packet_pairs),
        lambda packet_pairs: map(lambda packet_pair: packet_pair[0] + 1, packet_pairs),
        sum,
        str)


def part_2(raw_pairs_of_packets: list[str]) -> str:
    divider_packets = {Packet([[2]]), Packet([[6]])}
    return chain_functions(
        raw_pairs_of_packets,
        to_packets,
        lambda packets: chain(packets, divider_packets),
        sorted,
        enumerate,
        lambda packets: filter(lambda packet_and_index: packet_and_index[1] in divider_packets, packets),
        lambda packets: map(lambda packet_and_index: packet_and_index[0] + 1, packets),
        lambda packets: reduce(mul, packets),
        str
    )
