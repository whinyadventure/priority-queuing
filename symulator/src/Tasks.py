import json
from typing import List

from src.Task import *


class Tasks(object):
    tasks_list: List[Task]

    def __init__(self):
        self.tasks_list = []
        self.parameters = dict()

    @staticmethod
    def parse_line(line):
        return line.split(" ")

    @staticmethod
    def parse_parameters(line):
        return json.loads(line)

    def read_input_file(self, filename="input.txt"):
        with open(filename) as file:
            self.parameters = json.load(file)
            tasks_json = self.parameters.pop('tasks', None)
            for task_json in tasks_json:
                self.tasks_list.append(Task(task_json["id"], task_json["arrival"], task_json["size"], task_json["dt_max"]))

    def print(self):
        print("PARAMETERS: ", end="")
        for key, value in self.parameters.items():
            print(key, ":", value, end=" ")
        print("\nProcess list:")
        for i_task in self.tasks_list:
            print(i_task.to_string())

    def clear(self):
        for task in self.tasks_list:
            task.processed = 0.0
            task.processing_start = -1.0
            task.processing_end = -1.0


def calculate_statistics(process_list: List[Task], file=False, filename="stats.txt"):
    waiting_time = 0.0  # czas opoznienia
    turn_around_time = 0.0  # czas odpowiedz
    done_in_time_count = 0
    for process in process_list:
        waiting_time += process.get_waiting_time()
        turn_around_time += process.get_turn_around_time()
        if process.is_done_in_time():
            done_in_time_count += 1
    process_count = len(process_list)
    avg_late = round(waiting_time / process_count, 2)
    avg_latency = round(turn_around_time / process_count, 2)
    done_in_time_percent = round(100 * done_in_time_count / process_count, 2)
    avg_late = waiting_time / process_count
    avg_latency = turn_around_time / process_count
    done_in_time_percent = 100 * done_in_time_count / process_count
    print("Sredni_czas_opoznienia:", avg_late)
    print("Sredni_czas_odpowiedzi:", avg_latency)
    print("Zadania_obsluzone_w_czasie [%]:", done_in_time_percent)
    # todo write to file
    return avg_late, avg_latency, done_in_time_percent
