# -*- coding: utf-8 -*-
import os
import psutil
import subprocess
import multiprocessing


def get_pid(process_name):
    pid_list = []
    for p in psutil.process_iter():
        if p.pid in (os.getpid(), os.getppid()):
            pass
        elif process_name in p.name():
            pid_list.append(p.pid)
    return pid_list


def kill_process(pid, lock):
    # command = 'kill -9 {}'.format(pid)
    comand = 'taskkill /f /pid {}'.format(pid)
    lock.acquire()
    p = subprocess.Popen(comand, shell=True)
    p.wait()
    lock.release()


if __name__ == "__main__":
    pid_list = get_pid('python.exe')
    process_list = []
    lock = multiprocessing.Lock()
    for pid in pid_list:
        p = multiprocessing.Process(target=kill_process, args=(pid, lock))
        p.start()
        process_list.append(p)
    for process in process_list:
        process.join()
    if get_pid('python.exe'):
        print('Can not kill all python process')
    else:
        print('All python process have been killed.')