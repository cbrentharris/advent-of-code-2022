"""
Hill Climbing Algorithm
"""
import sys
import heapq


class Node(object):
    def __init__(self, id: [int, int], val: str):
        self.neighbors = set()
        self.id = id
        self.val = val

    def __repr__(self):
        return self.neighbors.__repr__() + " " + str(self.id) + " " + self.val

    def __lt__(self, other):
        return self.val < other.val

    def ordinal_value(self) -> int:
        if self.val == 'S':
            return ord('a')
        elif self.val == 'E':
            return ord('z')
        else:
            return ord(self.val)

    def can_go_to(self, other) -> bool:
        return other.ordinal_value() - self.ordinal_value() <= 1

    def potentially_add_neighbor(self, neighbor) -> None:
        if self.can_go_to(neighbor):
            self.neighbors.add(neighbor)


def init_neighbors(node: Node, node_index: dict[[int, int], Node], rows: int, cols: int,
                   map_nodes: list[list[str]]) -> None:
    x, y = node.id
    for i in range(1, -2, -2):
        if 0 <= x + i < rows:
            new_key = (x + i, y)
            if new_key not in node_index:
                node_index[new_key] = Node(new_key, map_nodes[new_key[0]][new_key[1]])
            neighbor = node_index[new_key]
            node.potentially_add_neighbor(neighbor)
        if 0 <= y + i < cols:
            new_key = (x, y + i)
            if new_key not in node_index:
                node_index[new_key] = Node(new_key, map_nodes[new_key[0]][new_key[1]])
            neighbor = node_index[new_key]
            node.potentially_add_neighbor(neighbor)


def djikstras(starts: set[str], target, height_map):
    map_nodes = list(map(lambda s: list(s.strip()), height_map))
    rows = len(map_nodes)
    cols = len(map_nodes[0])
    nodes_to_process = []
    dist = {}
    prev = {}
    node_index = {}

    end = None
    for row in range(rows):
        for col in range(cols):
            key = (row, col)
            if key not in node_index:
                node_index[key] = Node(key, map_nodes[row][col])
            node = node_index[key]
            init_neighbors(node, node_index, rows, cols, map_nodes)
            if node.val in starts:
                dist[node] = 0
                heapq.heappush(nodes_to_process, (dist[node], node))
            else:
                dist[node] = sys.maxsize
                prev[node] = None

            if node.val == target:
                end = node

    while len(nodes_to_process) > 0:
        node_to_process = heapq.heappop(nodes_to_process)[1]
        if node_to_process == end:
            return str(dist[node_to_process])
        for neighbor in node_to_process.neighbors:
            val = dist[node_to_process] + 1
            if val < dist[neighbor]:
                dist[neighbor] = val
                prev[neighbor] = node_to_process
                heapq.heappush(nodes_to_process, (dist[neighbor], neighbor))

    return str(dist[end])


def part_1(height_map: list[str]) -> str:
    return djikstras({'S'}, 'E', height_map)


def part_2(height_map: list[str]) -> str:
    return djikstras({'S', 'a'}, 'E', height_map)
