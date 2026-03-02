import re

# 1. 
print(re.search("[abc]", "apple"))

# 2. 
print(re.search("[0-9]", "Year 2025"))

# 3.
print(re.search("[A-Z]", "python"))

# 4. 
print(re.search("[^0-9]", "123a"))

# 5. 
print(re.search("[a-zA-Z]+", "Hello123"))