# -*- coding: utf-8 -*-
import timeit
import threading

print('Main thread id: {}'.format(threading.current_thread().name))

lock = threading.Lock()

def work(sign, lock):
    lock.acquire()
    print('{}: {} {}'.format(sign, threading.current_thread().name, timeit.timeit()))
    lock.release()


if __name__ == "__main__":
    thread_list = []
    start = timeit.timeit()
    for i in range(10):
        t = threading.Thread(target=work, args=(i, lock))
        thread_list.append(t)
        t.start()
    for thread in thread_list:
        thread.join()
    end = timeit.timeit()
    print(end - start)