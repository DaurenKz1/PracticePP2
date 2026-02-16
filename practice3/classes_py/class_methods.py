class Dog:
    def bark(self):
        return "Woof"

d1 = Dog()
print(d1.bark())

class Calculator:
    def add(self, a, b):
        return a + b

calc = Calculator()
print(calc.add(3, 5))

class Greeter:
    def greet(self, name):
        return "Hello " + name

g = Greeter()
print(g.greet("Dauren"))

class Square:
    def area(self, side):
        return side * side

sq = Square()
print(sq.area(4))
