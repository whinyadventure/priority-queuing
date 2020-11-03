from src.Processes import *


class Event(object):
    def __init__(self, time, process_id):
        self.time = time
        self.process_id = process_id


def basic_fcfs(processes: Processes):
    events = []
    process_list = processes.process_list
    time = process_list[0].start_time
    delay = 0
    total_idle_time = 0
    finish_time = 0
    for proc in process_list:
        time += delay
        idle_time = proc.start_time - time
        if idle_time > 0:
            events.append(Event(time, -1))
            time += idle_time
            total_idle_time += idle_time
        events.append(Event(time, proc.process_id))
        proc.processing_start = time
        proc.processing_end = time + proc.duration
        finish_time = proc.processing_end
        delay = proc.duration

    print("Idle time:", round(total_idle_time, 2), "Load:", round(1.0 - total_idle_time / finish_time, 2), "%")

    print("EVENTS:\nprocess_id processing_start")
    for ev in events:
        print(ev.process_id, ev.time)
    print()
    processes.print()
