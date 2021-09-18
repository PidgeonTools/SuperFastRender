import itertools as it

def fib():
    ''' A modified Fibonacci generator that starts at 1 and increments '''
    a, b = 1, 1
    while True:
        yield a
        b = a + b
        yield b
        a = a + b
