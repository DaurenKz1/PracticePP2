def my_function_name(fname):
  print(fname + " Refsnes")

my_function_name("Emil")
my_function_name("Tobias")
my_function_name("Linus")

def my_function(name): # name is a parameter
  print("Hello", name)

my_function("Emil") # "Emil" is an argument

def my_function2(fname, lname):
  print(fname + " " + lname)

my_function2("Emil", "Refsnes")

def my_function3(country = "Norway"):
  print("I am from", country)

my_function3("Sweden")
my_function3("India")
my_function3()
my_function3("Brazil")