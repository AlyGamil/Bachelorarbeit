# Using a Python dictionary to act as an adjacency list
graph = {
    '5': ['3', '7'],
    '3': ['2', '4'],
    '7': ['8'],
    '2': [],
    '4': ['8'],
    '8': []
}

visited = set()  # Set to keep track of visited nodes of graph.


def dfs(visited, node):  # function for dfs
    if node not in visited:
        print(node)
        visited.add(node)
        for neighbour in graph[node]:
            dfs(visited, neighbour)


# Driver Code
print("Following is the Depth-First Search")
dfs(visited, '5')
l1 = []
s1 = set()
s2 = set()
s1.add(1)
s1.add(2)
s2.add(2)
s2.add(1)
l1.append(s1)
# l1.append(s2)

print(s2 in l1)
print(s2)
print(s1)
