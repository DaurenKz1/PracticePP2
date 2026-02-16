class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)


x = Person("John", "Doe")
x.printname()

class Student(Person):
  pass

x = Student("Mike", "Olsen")
x.printname()


class Animal:
    def speak(self):
        return "Sound"

class Dog(Animal):
    pass

d1 = Dog()
print(d1.speak())
