n = int(input())


def even(no):
    counter = 0
    for counter in range(no):
        yield counter * 2


even_numbers = even(n)
for i in range(n):
    print(next(even_numbers))
