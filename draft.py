l1 = [(4, 'n3'), ('u', 'n1'), ('v', 'n0'), (3, 'n2')]

x = lambda y: y[1]
l1.sort(key=lambda y: y[1])
print(l1)
