import re

text = "Hello\nWorld"

# 1 
print(re.search("hello", text, re.IGNORECASE))

# 2 
print(re.search("^World", text, re.MULTILINE))

# 3 
print(re.search("Hello.*World", text, re.DOTALL))

# 4  
print(re.findall("hello", text, re.IGNORECASE))

# 5  
print(re.sub("hello", "Hi", text, re.IGNORECASE))