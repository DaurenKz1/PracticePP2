class Animal:
    def speak(self):
        return "Some sound"

class Dog(Animal):
    def speak(self):
        return "Woof"

d1 = Dog()
print(d1.speak())

class Person:
    def role(self):
        return "Person"

class Student(Person):
    def role(self):
        return "Student"

s1 = Student()
print(s1.role())
