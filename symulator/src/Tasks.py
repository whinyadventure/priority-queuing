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
    print("Sredni czas opoznienia:", round(waiting_time / process_count, 2))
    print("Sredni czas odpowiedzi:", round(turn_around_time / process_count, 2))
    print("Zadania obsluzone w czasie [%]:", round(100 * done_in_time_count / process_count, 2))
