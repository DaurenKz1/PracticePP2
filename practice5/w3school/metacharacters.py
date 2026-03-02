import re

# 1. 
print(re.search("c.t", "cat"))

# 2.
print(re.search("go*", "gooooal"))

# 3. 
print(re.search("go+", "goal"))

# 4. 
print(re.search("^Hello$", "Hello"))

# 5. 
print(re.search("cat|dog", "dog"))