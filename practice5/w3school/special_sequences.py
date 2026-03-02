import re

# 1.
print(re.search(r"\d", "Age 20"))

# 2. 
print(re.search(r"\w+", "Hello123"))

# 3. 
print(re.search(r"\s", "Hello World"))

# 4. 
print(re.search(r"\D+", "123abc"))

# 5.
print(re.search(r"\AHello", "Hello world"))