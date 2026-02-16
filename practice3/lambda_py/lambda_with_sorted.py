numbers_d = [5, 2, 9, 1]

sorted_numbers = sorted(numbers_d, key=lambda x: x)
print(sorted_numbers)   



words_c = ["apple", "hi", "banana", "cat"]

sorted_by_length = sorted(words_c, key=lambda word: len(word))
print(sorted_by_length)  



numbers_e = [23, 45, 12, 34]

sorted_by_last_digit = sorted(numbers_e, key=lambda num: num % 10)
print(sorted_by_last_digit)  



