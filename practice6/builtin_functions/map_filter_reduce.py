numbers = [1, 2, 3, 4, 5]

numbers2 = [1, 2, 3, 4, 5, 6]


squared = list(map(lambda x: x**2, numbers))
even = list(filter(lambda x: x % 2 == 0, numbers2))



print(squared)
print(even)