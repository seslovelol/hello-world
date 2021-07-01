# -*- coding: utf-8 -*-
import timeit
import multiprocessing

print('Main id: {}'.format(multiprocessing.current_process().name))

lock = multiprocessing.Lock()

def producer(queue):
    queue.put('{} put queue {}'.format(multiprocessing.current_process().name, timeit.timeit()))

def consumer(queue, lock):
    info = queue.get()
    lock.acquire()
    print('{} get queue {}'.format(multiprocessing.current_process().name, info))
    lock.release()

queue = multiprocessing.Queue(5)

queue_producer = []
queue_consumer = []

if __name__ == "__main__":
    for _ in range(10):
        process_producer = multiprocessing.Process(target=producer, args=(queue,))
        process_producer.start()
        queue_producer.append(process_producer)

    for _ in range(10):
        process_consumer = multiprocessing.Process(target=consumer, args=(queue, lock))
        process_consumer.start()
        queue_consumer.append(process_consumer)

    for p in queue_producer:
        p.join()

    queue.close()

    for c in queue_consumer:
        c.join()