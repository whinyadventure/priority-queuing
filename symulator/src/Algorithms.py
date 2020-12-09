from src.Tasks import *
from queue import PriorityQueue


class Event(object):
    def __init__(self, time, process_id):
        self.time = time
        self.process_id = process_id


def print_info(processes, events, total_idle_time, finish_time):
    print(f'Idle time: {total_idle_time} Finish time: {finish_time} '
          f'Load: {round(1.0 - total_idle_time / finish_time, 2)}')
    print('EVENTS:\nprocess_id processing_start')

    for ev in events:
        print(ev.process_id, ev.time)

    processes.print()


def do_task(task: Task, time: float, events):
    idle_time = task.arrival - time

    if idle_time > 0:
        events.append(Event(time, -1))  # dummy task
        time += idle_time

    events.append(Event(time, task.task_id))

    if task.processing_start < 0:
        task.processing_start = time
        task.processing_end = time + task.size
    else:
        task.processing_end = time + (task.size - task.processed)

    task.processed = task.size

    return max(0, idle_time), task.processing_end


def basic_fcfs(processes: Tasks):
    events = []
    tasks_list = processes.tasks_list
    time = tasks_list[0].arrival
    total_idle_time = 0

    for i_task in tasks_list:
        idle_time, time = do_task(i_task, time, events)
        total_idle_time += idle_time

    # print_info(processes, events, total_idle_time, time)


def do_poor_queue(poor_queue, next_task_arrival, time, events):
    while not poor_queue.empty():  # do tasks from poor queue as long as you can
        poor_task = poor_queue.get()[1]
        poor_task_end = min(time + (poor_task.size - poor_task.processed), next_task_arrival)
        poor_task.processed += (poor_task_end - time)  # how much more task done

        if poor_task.processing_start < 0:
            poor_task.processing_start = time  # the beginning of the first time the task being processed

        events.append(Event(time, poor_task.task_id))
        poor_task.processing_end = time = poor_task_end

        if not poor_task.is_done():
            poor_queue.put((poor_task.arrival, poor_task))

        if time == next_task_arrival:
            break

    return time, poor_queue


def enhanced_fcfs(processes: Tasks):
    events = []
    tasks_list = processes.tasks_list
    time = tasks_list[0].arrival
    total_idle_time = 0

    basic_queue = PriorityQueue()
    poor_queue = PriorityQueue()

    for task in tasks_list:
        basic_queue.put((task.arrival, task))

    while not basic_queue.empty():
        next_task = basic_queue.get()[1]

        if time > next_task.max_starting_time:
            poor_queue.put((next_task.arrival, next_task))
            continue

        if time < next_task.arrival:  # highest priority task has not arrived yet
            time, poor_queue = do_poor_queue(poor_queue, next_task.arrival, time, events)

        idle_time, time = do_task(next_task, time, events)
        total_idle_time += idle_time

    while not poor_queue.empty():
        next_task = poor_queue.get()[1]
        idle_time, time = do_task(next_task, time, events)
        total_idle_time += idle_time

    # print_info(processes, events, total_idle_time, time)


