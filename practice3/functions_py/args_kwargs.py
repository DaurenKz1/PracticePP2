def my_function_(*args):
  print("Type:", type(args))
  print("First argument:", args[0])
  print("Second argument:", args[1])
  print("All arguments:", args)

my_function_("Emil", "Tobias", "Linus")

def my_function2(greeting, *names):
  for name in names:
    print(greeting, name)

my_function2("Hello", "Emil", "Tobias", "Linus")

def my_function(*numbers):
  total = 0
  for num in numbers:
    total += num
  return total

print(my_function(1, 2, 3))
print(my_function(10, 20, 30, 40))
print(my_function(5))

def my_function1(**myvar):
  print("Type:", type(myvar))
  print("Name:", myvar["name"])
  print("Age:", myvar["age"])
  print("All data:", myvar)

my_function1(name = "Tobias", age = 30, city = "Bergen")

def print_user(**kwargs):
    for key, value in kwargs.items():
        print(key, ":", value)

print_user(name="Dauren", city="Almaty", university="KBTU")
