# -*-coding: utf-8 -*-

import timeit
import functools

def clock(func):
    functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = timeit.default_timer()
        result = func(*args, **kwargs)
        elapsed = timeit.default_timer() - t0
        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(','.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['{}={}'.format((k, v) for k, v in sorted(kwargs.items()))]
            arg_lst.append(','.join(pairs))
        arg_str = ','.join(arg_lst)
        print('[{:.8f}]{}({}) -> {}'.format(elapsed, name, arg_str, result))
        return result
    return clocked