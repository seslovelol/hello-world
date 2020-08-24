# -*- coding: utf-8 --

import functools
from clock import clock

class Fibs:
    def __init__(self):
        self.a = 0
        self.b = 1
    @clock
    def __next__(self):
        self.a, self.b = self.b, self.a + self.b
        return self.a
    def __iter__(self):
        return self

@functools.lru_cache()
@clock
def fibonacci(n):
    if n < 2:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)


def flatten(nested):
    try:
        try: nested + ''
        except TypeError: pass
        else: raise TypeError
        for element in nested:
            for e in flatten(element):
                yield e
    except TypeError:
        yield nested


if __name__ == "__main__":
    fib = Fibs()
    for f in fib:
        if f > 1000:
            print(f)
            break
    fibonacci(17)
    nested = [1, [2, 3], [5], 'string', [6, [7, [8, 8, 'str']]]]
    for n in flatten(nested):
        print(n)