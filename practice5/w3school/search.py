import re

text = "I love Python and Python loves me"

# 1
print(re.search("Python", text))

# 2
print(re.search("love", text))

# 3
print(re.search(r"\d+", "Age 18"))

# 4
print(re.search("^I", text))

# 5
print(re.search("me$", text))