class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, grade):
        super().__init__(name)
        self.grade = grade

s1 = Student("Ali", 90)
print(s1.name, s1.grade)


class Animal:
    def __init__(self, type):
        self.type = type

class Dog(Animal):
    def __init__(self, type, name):
        super().__init__(type)
        self.name = name

d1 = Dog("Mammal", "Rex")
print(d1.type, d1.name)
