# -*- coding: utf-8 -*-
import timeit
import multiprocessing

print('Main id: {}'.format(multiprocessing.current_process().name))

pipe = multiprocessing.Pipe()

def pipe1(pipe):
    pipe.send('Ping {}'.format(timeit.timeit()))
    print(pipe.recv())

def pipe2(pipe):
    print(pipe.recv())
    pipe.send('Pang {}'.format(timeit.timeit()))

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=pipe1, args=(pipe[0],))
    p2 = multiprocessing.Process(target=pipe2, args=(pipe[1],))
    p1.start()
    p2.start()
    p1.join()
    p2.join()