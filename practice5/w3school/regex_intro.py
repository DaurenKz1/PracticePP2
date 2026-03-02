import re

# 1.
text = "I love Python"
print(re.search("Python", text))

# 2.
text = "My age is 18"
print(re.search(r"\d", text))

# 3.
text = "Email: test@gmail.com"
print(re.search(r"\S+@\S+", text))

# 4. 
text = "The cat is sleeping"
print(re.search("cat", text))

# 5.
text = "Hello world"
print(re.search("^Hello", text))