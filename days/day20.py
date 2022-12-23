"""
Grove Positioning System
"""
from itertools import cycle


class Node(object):
    def __init__(self, id: int, value: int):
        self.prev = None
        self.next = None
        self.value = value
        self.id = id

    def __str__(self):
        return "ID: {}, Value: {}".format(self.id, self.value)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


class Decrypter(object):
    def __init__(self, encrypted_numbers: list[int], decryption_key=1):
        nodes = list(map(lambda p: Node(*p), enumerate(map(lambda i: i * decryption_key, encrypted_numbers))))
        self.head = nodes[0]

        def circular_pairwise(l):
            second = cycle(l)
            next(second)
            return zip(l, second)

        for a, b in circular_pairwise(nodes):
            a.next = b
            b.prev = a
            if a.value == 0:
                self.zero = a
        self.length = len(nodes)
        self.nodes = nodes

    def decrypt(self, mixes=1):
        for i in range(mixes):
            for node in self.nodes:
                self.__mix__(node)

    def find_after_zero(self, index: int):
        return self.find_offset(index % self.length, self.zero)

    def find_coordinate_sum(self):
        return sum(map(lambda i: self.find_after_zero(i).value, range(1000, 4000, 1000)))

    @staticmethod
    def find_offset(delta, node):
        iterations = 0
        curr = node
        if delta > 0:
            while iterations < delta:
                curr = curr.next
                iterations += 1
        elif delta < 0:
            while iterations < abs(delta):
                curr = curr.prev
                iterations += 1

        return curr

    def __mix__(self, node) -> None:
        moves = node.value % (self.length - 1)
        if moves == 0:
            return

        original_node_next = node.next
        original_node_prev = node.prev

        if node == self.head:
            self.head = node.next

        if moves > 0:
            curr = self.find_offset(moves, node)
        else:
            curr = self.find_offset(moves, node.prev)
        if original_node_next.id == curr.next.id:
            return
        original_node_next.prev = original_node_prev
        original_node_prev.next = original_node_next

        curr_next = curr.next
        curr.next = node
        node.prev = curr
        node.next = curr_next
        curr_next.prev = node

    def __str__(self):
        return str(list(map(lambda n: n.value, self.as_list())))

    def __repr__(self):
        return self.__str__()

    def as_list(self):
        nodes = []
        curr = self.head
        while len(nodes) != self.length:
            nodes.append(curr)
            curr = curr.next
        return nodes


def part_1(raw_numbers: list[str]) -> str:
    encrypted_numbers = list(map(int, map(lambda s: s.strip(), raw_numbers)))
    decrypter = Decrypter(encrypted_numbers)
    decrypter.decrypt()
    return str(decrypter.find_coordinate_sum())


def part_2(raw_numbers: list[str]) -> str:
    decryption_key = 811589153
    encrypted_numbers = list(map(int, map(lambda s: s.strip(), raw_numbers)))
    decrypter = Decrypter(encrypted_numbers, decryption_key=decryption_key)
    decrypter.decrypt(mixes=10)
    return str(decrypter.find_coordinate_sum())
