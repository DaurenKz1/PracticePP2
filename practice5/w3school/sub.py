import re

# 1
print(re.sub("cat", "dog", "I have a cat"))

# 2
print(re.sub(r"\d+", "NUMBER", "Age 18"))

# 3
print(re.sub(" ", "-", "Hello World"))

# 4
print(re.sub(r"[aeiou]", "*", "hello"))

# 5
print(re.sub("Python", "Java", "Python is cool"))