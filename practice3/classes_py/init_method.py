class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

p1 = Person("Emil", 36)

print(p1.name)
print(p1.age)


class Car:
    def __init__(self, brand, year):
        self.brand = brand
        self.year = year

car1 = Car("Toyota", 2022)
print(car1.brand, car1.year)

class Phone:
    def __init__(self, model):
        self.model = model

phone1 = Phone("iPhone")
print(phone1.model)
