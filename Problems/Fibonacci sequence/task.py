def fibonacci(n):
    a = 0
    b = 1
    if n >= 1:
        yield a
    if n >= 2:
        yield b
    for i in range(2, n):
        a, b = b, a + b
        yield b
