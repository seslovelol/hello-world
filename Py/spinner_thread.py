# -*- coding: utf-8 -*-
import time
import threading
import itertools

def spin(msg, done):
    status = ''
    for char in itertools.cycle('-|/\\'):
        status = char + ' ' + msg
        print(status, flush=True, end='\r')
        if done.wait(.1):
            break
    print(' ' * len(status))

def slow_function():
    time.sleep(3)
    return 88

def supervisor():
    msg = 'Thinking !'
    done = threading.Event()
    spinner = threading.Thread(target=spin, args=(msg, done))
    print('spinner:', spinner)
    spinner.start()
    result = slow_function()
    done.set()
    spinner.join()
    return result

def main():
    result = supervisor()
    print('Answer:', result)

if __name__ == "__main__":
    main()