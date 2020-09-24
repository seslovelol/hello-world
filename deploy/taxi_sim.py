# -*- coding: utf-8 -*-
import queue
import random
from collections import namedtuple

DEFAULT_NUMBER_OF_TAXIS = 3
DEFAULT_END_TIME = 180
SEARCH_DERATION = 5
TRIP_DERATION = 20
DEPARTURE_INTERVAL = 5
Event = namedtuple('Event', 'time proc action')
def taxi_proc(proc_id, trip, start_time):
    time = yield Event(start_time, proc_id, 'leave')
    for i in range(trip):
        time = yield Event(time, proc_id, 'pick up')
        time = yield Event(time, proc_id, 'drop off')
    time = yield Event(time, proc_id, 'go home')

class Simlarator():
    def __init__(self, proc_map):
        self.events = queue.PriorityQueue()
        self.procs = dict(proc_map)
    def run(self, end_time):
        for _, proc in sorted(self.procs.items()):
            first_event = next(proc)
            self.events.put(first_event)
        sim_time = 0
        while sim_time < end_time:
            if self.events.empty():
                print('*** end of events ***')
                break
            current_event = self.events.get()
            sim_time, proc_id, previous_action = current_event
            print('taxi id:', proc_id, '   '*proc_id, current_event)
            next_time = sim_time + compute_duration(previous_action)
            try:
                next_event = self.procs[proc_id].send(next_time)
            except StopIteration:
                del self.procs[proc_id]
            else:
                self.events.put(next_event)
        else:
            print('{} events pending.'.format(self.events.qsize()))

def compute_duration(previous_action):
    if previous_action in ['leave', 'drop off']:
        interval = SEARCH_DERATION
    elif previous_action == 'pick up':
        interval = TRIP_DERATION
    elif previous_action == 'go home':
        interval = 1
    else:
        raise ValueError('Unknown previous action {}'.format(previous_action))
    return int(random.expovariate(1/interval))

def main(end_time = DEFAULT_END_TIME):
    taxis = {i: taxi_proc(i, 2*(i+1), i*DEPARTURE_INTERVAL) for i in range(DEFAULT_NUMBER_OF_TAXIS)}
    sim = Simlarator(taxis)
    sim.run(end_time)

if __name__ == "__main__":
    main()