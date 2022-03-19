import pprint
from itertools import product

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

l1, l2 = [1, 2, 3], ['a', 'b']


# output = list(product(l1, l2))


def foo(*args):
    output = list(product(*args))
    return output


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


def heap_permutation(elements_to_permute, size):
    if size == 1:
        yield elements_to_permute

    for i in range(size):
        yield from heap_permutation(elements_to_permute.copy(), size - 1)

        if size & 1:
            elements_to_permute[0], elements_to_permute[size - 1] \
                = elements_to_permute[size - 1], elements_to_permute[0]
        else:
            elements_to_permute[i], elements_to_permute[size - 1] \
                = elements_to_permute[size - 1], elements_to_permute[i]


