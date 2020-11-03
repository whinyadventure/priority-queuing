from src.Tasks import *


class Event(object):
    def __init__(self, time, process_id):
        self.time = time
        self.process_id = process_id


def basic_fcfs(processes: Tasks):
    events = []
    tasks_list = processes.tasks_list
    time = tasks_list[0].start_time
    delay = 0
    total_idle_time = 0
    finish_time = 0
    for i_task in tasks_list:
        time += delay
        idle_time = i_task.start_time - time
        if idle_time > 0:
            events.append(Event(time, -1))
            time += idle_time
            total_idle_time += idle_time
        events.append(Event(time, i_task.task_id))
        i_task.processing_start = time
        i_task.processing_end = time + i_task.duration
        finish_time = i_task.processing_end
        delay = i_task.duration

    print("Idle time:", round(total_idle_time, 2), "Load:", round(1.0 - total_idle_time / finish_time, 2), "%")

    print("EVENTS:\nprocess_id processing_start")
    for ev in events:
        print(ev.process_id, ev.time)
    print()
    processes.print()
