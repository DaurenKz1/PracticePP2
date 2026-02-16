numbers_a = [1, 2, 3, 4, 5, 6]

even_numbers = list(filter(lambda x: x % 2 == 0, numbers_a))
print(even_numbers)  

numbers_b = [5, 12, 7, 20, 3]

greater_than_ten = list(filter(lambda y: y > 10, numbers_b))
print(greater_than_ten)   


words_b = ["hi", "python", "cat", "code"]

long_words = list(filter(lambda word: len(word) > 3, words_b))
print(long_words)   

numbers_c = [-5, 3, -1, 8, 0]

positive_numbers = list(filter(lambda num: num > 0, numbers_c))
print(positive_numbers)   
