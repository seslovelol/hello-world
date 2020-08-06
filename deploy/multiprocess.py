# -*- coding: utf-8 -*-
import os
import time
import threading
import multiprocessing

print('Main id: {}'.format(os.getpid()))

def work(sign, lock):
    lock.acquire()
    print(sign, os.getpid())
    lock.release()

p_lock = multiprocessing.Lock()

t_lock = threading.Lock()

t_list = []
p_list = []

def pipe1(pipe):
    pipe.send('hello1')
    print(pipe.recv())


def pipe2(pipe):
    print(pipe.recv())
    pipe.send('hello2')


pipe = multiprocessing.Pipe()

def inqueue(queue):
    queue.put('{} put queue {}'.format(os.getpid(), time.time()))

def outqueue(queue, lock):
    info = queue.get()
    lock.acquire()
    print('{} get queue {}'.format(os.getpid(), info))
    lock.release()

queue = multiprocessing.Queue(5)

inq_list = []
outq_list = []

if __name__ == "__main__":
    # multi Thread
    # for _ in range(5):
    #     t = threading.Thread(target=work, args=('thread', t_lock))
    #     t.start()
    #     t_list.append(t)
    # for t in t_list:
    #     t.join()
    # # multi Process
    # for _ in range(5):
    #     p = multiprocessing.Process(target=work, args=('process', p_lock))
    #     p.start()
    #     p_list.append(p)
    # for p in p_list:
    #     p.join()
    # # PIPE
    # p1 = multiprocessing.Process(target=pipe1, args=(pipe[0],))
    # p2 = multiprocessing.Process(target=pipe2, args=(pipe[1],))
    # p1.start()
    # p2.start()
    # p1.join()
    # p2.join()
    # queue
    for _ in range(10):
        q1 = multiprocessing.Process(target=inqueue, args=(queue,))
        q1.start()
        inq_list.append(q1)

    for _ in range(10):
        q2 = multiprocessing.Process(target=outqueue, args=(queue, p_lock))
        q2.start()
        outq_list.append(q2)

    for inq in inq_list:
        inq.join()

    queue.close()

    for outq in outq_list:
        outq.join()