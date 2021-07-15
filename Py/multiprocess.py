# -*- coding: utf-8 -*-
import timeit
import multiprocessing

print('Main id: {}'.format(multiprocessing.current_process().name))

lock = multiprocessing.Lock()

def work(sign, lock):
    lock.acquire()
    print('{}: {} {}'.format(sign, multiprocessing.current_process().name, timeit.timeit()))
    lock.release()


if __name__ == "__main__":
    process_list = []
    start = timeit.timeit()
    for i in range(10):
        process = multiprocessing.Process(target=work, args=(i, lock))
        process.start()
        process_list.append(process)
    for p in process_list:
        p.join()
    end = timeit.timeit()
    print(end - start)