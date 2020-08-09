# -*- coding: utf-8 --

class Fibs:
    def __init__(self):
        self.a = 0
        self.b = 1

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b
        return self.a

    def __iter__(self):
        return self


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
    nested = [1, [2, 3], [5], 'string', [6, [7, [8, 8, 'str']]]]
    for n in flatten(nested):
        print(n)