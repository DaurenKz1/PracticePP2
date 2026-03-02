import re

# 1
print(re.match("Hello", "Hello world"))

# 2
print(re.match("world", "Hello world"))

# 3
print(re.match(r"\d+", "123abc"))

# 4
print(re.match(r"[A-Z]", "Python"))

# 5
print(re.match("cat", "dog cat"))