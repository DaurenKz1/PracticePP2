import re

# 1
print(re.split(",", "apple,banana,orange"))

# 2
print(re.split(r"\s+", "Hello   World"))

# 3
print(re.split("-", "2025-03-02"))

# 4
print(re.split(r"\d+", "Hello123World456"))

# 5
print(re.split("a", "banana"))