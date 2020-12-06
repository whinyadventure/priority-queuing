from src.Tasks import *
from queue import PriorityQueue


class Event(object):
    def __init__(self, time, process_id):
        self.time = time
        self.process_id = process_id


def print_info(processes, events, total_idle_time, finish_time):
    print("Idle time:", total_idle_time,"Finish time:",finish_time, "Load:", round(1.0 - total_idle_time / finish_time, 2), "")
    print("EVENTS:\nprocess_id processing_start")
    for ev in events:
        print(ev.process_id, ev.time)
    processes.print()


def basic_fcfs(processes: Tasks):
    events = []
    tasks_list = processes.tasks_list
    time = tasks_list[0].arrival
    delay = 0
    total_idle_time = 0
    finish_time = 0
    for i_task in tasks_list:
        time += delay
        idle_time = i_task.arrival - time
        if idle_time > 0:
            events.append(Event(time, -1))
            time += idle_time
            total_idle_time += idle_time
        events.append(Event(time, i_task.task_id))
        i_task.processing_start = time
        i_task.processing_end = time + i_task.size
        i_task.processed = i_task.processing_end - i_task.processing_start
        finish_time = i_task.processing_end
        delay = i_task.size
    #print_info(processes, events, total_idle_time, finish_time)
    #processes.print()

def is_late(process: Task, time: float):
    return time > process.max_starting_time


def do_poor_queue(poor_queue, next_task_arrival, time,  events, alg_version):
    while not poor_queue.empty():  # do tasks from poor queue as long as you can
        poor_task = poor_queue.get()[1]
        poor_task_left = poor_task.size - poor_task.processed  # how much task left to process
        poor_task_end = min(time + poor_task_left, next_task_arrival)
        poor_task.processed += (poor_task_end - time)  # how much more task done
        if poor_task.processing_start <= 0.0:
            poor_task.processing_start = time  # the beginning of the first time the task being processed
        events.append(Event(time, poor_task.task_id))
        time = poor_task_end
        poor_task.processing_end = time
        if not poor_task.is_done():
            put_task(poor_queue, poor_task, alg_version)
        if time >= next_task_arrival:
            break
    return time, poor_queue


#todo clean up the code
#todo more testing
def super_fcfs(processes: Tasks):
    events = []
    tasks_list = processes.tasks_list
    time = tasks_list[0].arrival
    total_idle_time = 0
    finish_time = 0
    basic_queue = PriorityQueue()
    poor_queue = PriorityQueue()
    for task in tasks_list:
        put_task(basic_queue, task, alg_version)
    while not basic_queue.empty():
        next_task = basic_queue.get()[1]
        next_task_arrival = next_task.arrival
        if is_late(next_task, time):
            put_task(poor_queue, next_task, alg_version)
            continue
        if time < next_task_arrival:  # highest priority task has not arrived yet
            time, poor_queue = do_poor_queue(poor_queue, next_task_arrival, time, events, alg_version)
        idle_time, finish_time = do_task(next_task, time, events)
        total_idle_time += idle_time
        time += next_task.size

    while not poor_queue.empty():
        next_task = poor_queue.get()[1]
        idle_time = next_task.arrival - time
        if idle_time > 0:
            events.append(Event(time, -1))
            time += idle_time
            total_idle_time += idle_time
        events.append(Event(time, next_task.task_id))
        next_task.processing_start = time
        next_task.processing_end = time + next_task.size
        finish_time = next_task.processing_end
        time += next_task.size
    print("Idle time:", round(total_idle_time, 2), "Load:", round(1.0 - total_idle_time / finish_time, 2), "%")
    print("EVENTS:\nprocess_id processing_start")
    for ev in events:
        print(ev.process_id, ev.time)
    print()
    processes.print()
