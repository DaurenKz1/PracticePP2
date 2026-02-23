
#1
def square_numbers(num):
    for i in range(1, num+1):
        yield i * i

user_in = int(input())
for i in square_numbers(user_in):
    print(i)


#2
def even_numbers(n):
    for i in range(0, n+1, 2):
        yield i

user_in1 = int(input())

print(*even_numbers(user_in), sep=", ")

#3
def divisible_by_3_and_4(n):
    for i in range(0, n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i


user_in2 = int(input())

print(*divisible_by_3_and_4(user_in2), sep=",")

#4
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i


a = int(input("Enter a: "))
b = int(input("Enter b: "))

for value in squares(a, b):
    print(value)

#5
def countdown(n):
    for i in range(n, -1, -1):
        yield i


n = int(input("Enter n: "))

for number in countdown(n):
    print(number)