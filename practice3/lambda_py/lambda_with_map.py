numbers1 = [1, 2, 3, 4]

triple_numbers = list(map(lambda x: x * 3, numbers1))
print(triple_numbers)   


numbers2 = [2, 4, 6]

squared_numbers = list(map(lambda y: y ** 2, numbers2))
print(squared_numbers)  

numbers3 = [10, 20, 30]

string_numbers = list(map(lambda z: str(z), numbers3))
print(string_numbers)

words_list = ["cat", "elephant", "hi"]

word_lengths = list(map(lambda word: len(word), words_list))
print(word_lengths)   


