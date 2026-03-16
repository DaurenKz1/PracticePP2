names = ["Alice", "Bob", "Charlie"]


names_ = ["Alice", "Bob", "Charlie"]
scores = [90, 85, 88]


for index, name in enumerate(names):
    print(index, name)


for name_, score in zip(names_, scores):
    print(name_, score)