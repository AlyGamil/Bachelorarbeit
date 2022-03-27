import itertools
import pprint

# one = TopologyNode.get_node('1')
# two = TopologyNode.get_node('2')
# three = TopologyNode.get_node('3')
# four = TopologyNode.get_node('4')
# five = TopologyNode.get_node('5')
# six = TopologyNode.get_node('6')
# seven = TopologyNode.get_node('7')
# u = TopologyNode.get_node('u')
# v = TopologyNode.get_node('v')
# w = TopologyNode.get_node('w')
# n1 = ConfigurationNode.get_node('n1')
# n2 = ConfigurationNode.get_node('n2')
# n3 = ConfigurationNode.get_node('n3')


# u = TopologyNode.get_node('u')
# v = TopologyNode.get_node('v')
# drei = TopologyNode.get_node('3')
# vier = TopologyNode.get_node('4')
# zero = TopologyNode.get_node('0')
# sieben = TopologyNode.get_node('7')
# n1 = ConfigurationNode.get_node('n1')
# n2 = ConfigurationNode.get_node('n2')
# n3 = ConfigurationNode.get_node('n3')
# n0 = ConfigurationNode.get_node('n0')
# test = [u, drei, v, vier]
# print(element_same_direction([zero, sieben], [n0, n3]))
from fontTools.misc.py23 import xrange


def swap(seq, i, j):
    seq[i], seq[j] = seq[j], seq[i]


def generate_permutations(seq, sequence_length, result_length):
    c = [0] * sequence_length
    yield seq[:result_length]

    i = 0
    while i < sequence_length:
        if c[i] < i:
            if i % 2 == 0:
                swap(seq, 0, i)
            else:
                swap(seq, c[i], i)

            yield seq[:result_length]
            c[i] += 1
            i = 0
        else:
            c[i] = 0
            i += 1


def permutations(seq, resLen=None):
    if not resLen: resLen = len(seq)
    return generate_permutations(seq, len(seq), resLen)


def all_perms(elements):
    if len(elements) <= 1:
        yield elements
    else:

        for perm in all_perms(elements[1:]):
            for i in range(len(elements)):
                yield perm[:i] + elements[0:1] + perm[i:]


generated_permutations = []


def recursive_heaps_algorithm(elements_to_permute, length):
    if length == 1:
        generated_permutations.append(elements_to_permute)
    else:

        length -= 1
        recursive_heaps_algorithm(elements_to_permute.copy(), length)
        for i in range(length):
            if length & 1:
                swap(elements_to_permute, 0, length)
            else:
                swap(elements_to_permute, i, length)

            recursive_heaps_algorithm(elements_to_permute.copy(), length)


level = 0


def simple_permutation(elements_to_permute, current_permutation=None):
    current_permutation = [] if not current_permutation else current_permutation
    if elements_to_permute:
        for e in elements_to_permute:
            current_permutation.append(e)
            next_permutation = current_permutation
            remaining_elements = elements_to_permute.copy()
            remaining_elements.remove(e)
            yield from simple_permutation(elements_to_permute=remaining_elements, current_permutation=next_permutation)
            next_permutation.pop()
    else:
        yield current_permutation.copy()


graph = {
    '5': ['3', '7'],
    '3': ['2', '4'],
    '7': ['8'],
    '2': [],
    '4': ['8'],
    '8': []
}

visited = []  # List for visited nodes.
queue = []  # Initialize a queue


def bfs(visited, graph, node):  # function for BFS
    visited.append(node)
    queue.append(node)
    x = visited
    y = queue
    while queue:  # Creating loop to visit each node
        m = queue.pop(0)
        print(m, end=" ")

        for neighbour in graph[m]:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)


def get_combinations(layouts):
    results = []
    for i in range(1, len(layouts) + 1):
        results.extend(list(itertools.combinations(layouts, i)))
    return results


x = [1, 2, 3]
y = [1, 2, 3]
print((set(x), set(y)))

