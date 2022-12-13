"""
Distress Signal
"""
import json
from functools import reduce
from itertools import chain as ichain
from operator import mul
from typing import Iterable, Union

from day3 import chunk
from days.local_functools import chain


class Packet(object):
    def __init__(self, items: list):
        self.items = items

    def __lt__(self, other):
        return self.less_than(self.items, other.items)

    def less_than(self, left, right) -> Union[None, bool]:
        if type(left) == type(right) == int:
            if left < right:
                return True
            elif right < left:
                return False
            else:
                return None
        if type(left) == type(right) == list:
            if len(left) == len(right) == 0:
                return None
            if len(left) == 0:
                return True
            if len(right) == 0:
                return False
            for i in range(len(left)):
                if i >= len(right):
                    return False
                left_child = left[i]
                right_child = right[i]
                child_result = self.less_than(left_child, right_child)
                if child_result:
                    return True
                if child_result is not None:
                    return False
            if len(left) < len(right):
                return True
            return None
        else:
            if type(left) == int:
                return self.less_than([left], right)
            else:
                return self.less_than(left, [right])


def to_packets(raw_packets: Iterable[str]) -> Iterable[Packet]:
    return chain(raw_packets,
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

    return chain(raw_pairs_of_packets,
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
    return chain(
        raw_pairs_of_packets,
        to_packets,
        lambda packets: ichain(packets, divider_packets),
        sorted,
        enumerate,
        lambda packets: filter(lambda packet_and_index: packet_and_index[1] in divider_packets, packets),
        lambda packets: map(lambda packet_and_index: packet_and_index[0] + 1, packets),
        lambda packets: reduce(mul, packets),
        str
    )
