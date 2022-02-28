a = [1, 2, 3, 4, 5]
b = [9, 8, 7, 6, 5]

x = [i for i, j in zip(a, b) if i == j]
print(x)