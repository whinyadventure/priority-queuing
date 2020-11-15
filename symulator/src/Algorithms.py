from src.Tasks import *
from queue import PriorityQueue


class Event(object):
    def __init__(self, time, process_id):
        self.time = time
        self.process_id = process_id


def print_info(processes, events, total_idle_time, finish_time):
    print("Idle time:", round(total_idle_time, 2), "Load:", round(1.0 - total_idle_time / finish_time, 2), "%")
    print("EVENTS:\nprocess_id processing_start")
    for ev in events:
        print(ev.process_id, ev.time)
    print()
    processes.print()


def basic_fcfs(processes: Tasks):
    events = []
    tasks_list = processes.tasks_list
    time = tasks_list[0].arrival
    delay = 0
    total_idle_time = 0
    finish_time = 0
    print("Algorithm: super fcfs")
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
        finish_time = i_task.processing_end
        delay = i_task.size
    print_info(processes, events, total_idle_time, finish_time)


def is_late(process: Task, time: float):
    return time > process.max_starting_time


def super_fcfs(processes: Tasks):
    events = []
    tasks_list = processes.tasks_list
    time = tasks_list[0].arrival
    total_idle_time = 0
    finish_time = 0
    basic_queue = PriorityQueue()
    poor_queue = PriorityQueue()
    print("Algorithm: supers fcfs")
    for task in tasks_list:
        basic_queue.put((task.arrival, task))  # w tym drugim algorytmie task.max_end_time

    while not basic_queue.empty():
        next_task = basic_queue.get()[1]
        next_task_arrival = next_task.arrival
        while time < next_task_arrival:  # rob zadania z poor queue dopoki nie pojawi sie zadanie z basic_queue

            idle_time = next_task_arrival - time
            events.append(Event(time, -1))
            time += idle_time
            total_idle_time += idle_time
            if False:
                while not poor_queue.empty():
                    poor_task = poor_queue.get()[1]
                    poor_task_left = poor_task.size-poor_task.processed # ile zadania jeszcze trzeba wykonać
                    poor_task_end = min(time + poor_task_left, next_task_arrival)

                    events.append(Event(time, poor_task.task_id))
                    poor_task.processed+=poor_task_left-time
                    poor_task.processing_start = min(time, poor_task.processing_start)
                    poor_task.processing_end = time + poor_task_end
                    finish_time = poor_task.processing_end
                    time += poor_task_end
                    if not poor_task.is_done():
                        poor_queue.put(poor_task)


                    #to ponizej raczej do wywalenia
                    '''to_process = next_task_arrival-(time + poor_task_left)
                    if time + poor_task_left < next_task_arrival: #zdaze dokonczyc przed przybyciem
                        events.append(Event(time, poor_task.task_id))
                        poor_task.processing_start = time
                        poor_task.processing_end = time + poor_task_left
                        finish_time = poor_task.processing_end
                        time += poor_task.size
                    else:
                        events.append(Event(time, poor_task.task_id))
                        poor_task.processing_start = time
                        poor_task.processing_end = time + to_process
                        finish_time = poor_task.processing_end
                        time += poor_task.size
                        pass
                        #zrob tyle ile sie da
                        #wstaw do kolejki poor'''

        if is_late(next_task, time):
            poor_queue.put((next_task_arrival, next_task))  # w tym drugim algorytmie task.max_end_time
        else:  # wykonaj to zadanie
            events.append(Event(time, next_task.task_id))
            next_task.processing_start = time
            next_task.processing_end = time + next_task.size
            finish_time = next_task.processing_end
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

    '''
    dodaj wszystkie zadania do basic queue (posortowane)
    while basic_queue is not empty:
        basic_queue_start_for_next_task = basic_queue.peek().start_time
        if basic_queue_start_for_next_task >=current_time:
            tmp = basic_queue.pop()
            if check_basic_queue_condition(tmp, time) is False:
                poor_queue.add(tmp)
            else:
                tmp zaznacz jako wykonane [uzupelnij pola]
                current_time+= tmp.size
        else:
            wykonuj zadania z poor_queue i  do czasu basic_queue_start_for_next_task
    wykonaj wszystkie zadania z basic queue 
    '''
    print("Idle time:", round(total_idle_time, 2), "Load:", round(1.0 - total_idle_time / finish_time, 2), "%")
    print("EVENTS:\nprocess_id processing_start")
    for ev in events:
        print(ev.process_id, ev.time)
    print()
    processes.print()
