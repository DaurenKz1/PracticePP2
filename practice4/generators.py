
def square_numbers(num):
    for i in range(1, num+1):
        yield i * i

user_in = int(input())
for i in square_numbers(user_in):
    print(i)
