# -*-coding: utf-8 -*-
import time
import timeit
import multiprocessing


def test(msg):
    name = multiprocessing.current_process().name
    print(name, msg)
    return msg**2

if __name__ == "__main__":
    count = multiprocessing.cpu_count()
    pool1 = multiprocessing.Pool(count)
    pool2 = multiprocessing.Pool(count)
    result1 = []
    result2 = []
    start1 = timeit.default_timer()
    for i in range(8):
        p1 = pool1.apply(test, (i,))    # 同步
        result1.append(p1)
    pool1.close()
    pool1.join()
    end1 = timeit.default_timer()
    for r in result1:
        print(r)
    print(end1 - start1)

    start2 = timeit.default_timer()
    for i in range(8):
        p2 = pool2.apply_async(test, (i,))    # 异步
        result2.append(p2)
    pool2.close()
    pool2.join()
    end2 = timeit.default_timer()
    for r in result2:
        print(r.get())
    print(end2 - start2)
