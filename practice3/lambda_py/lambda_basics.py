x = lambda a : a + 10
print(x(5))

square = lambda x: x * x
print(square(4))  


def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)

print(mydoubler(11))
