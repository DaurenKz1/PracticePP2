import re

# 1. 
print(re.search(r"\d{3}", "1234"))

# 2. 
print(re.search(r"\d{2,}", "9 99 999"))

# 3. 
print(re.search(r"\d{2,4}", "12345"))

# 4. 
print(re.search(r"[a-z]{5}", "hello123"))

# 5.
print(re.search(r"a{1,3}", "aaab"))