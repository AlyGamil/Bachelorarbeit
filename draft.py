def generator():
    for i in range(10):
        yield i
    for j in range(10, 20):
        yield j


print(list(generator()))
