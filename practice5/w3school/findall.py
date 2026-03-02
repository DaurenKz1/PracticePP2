import re

text = "Python is fun. Python is powerful."

# 1
print(re.findall("Python", text))

# 2
print(re.findall(r"\w+", text))

# 3
print(re.findall(r"\d+", "1 22 333"))

# 4
print(re.findall(r"[A-Z]", text))

# 5
print(re.findall(r"is", text))