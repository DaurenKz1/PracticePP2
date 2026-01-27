a = 5
b = 2
if a > b: print("a is greater than b")


d = 2
c = 330
print("D") if d > c else print("C")

a1 = 10
b1 = 20
bigger = a1 if a1 > b1 else b1
print("Bigger is", bigger)


a2 = 330
b2 = 330
print("A2") if a2 > b2 else print("=") if a2 == b2 else print("B2")

x = 15
y = 20
max_value = x if x > y else y
print("Maximum value:", max_value)


username = ""
display_name = username if username else "Guest"
print("Welcome,", display_name)