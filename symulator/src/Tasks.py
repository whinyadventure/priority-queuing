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

    def read_input_file(self, filename="input.txt", use_const=True):
        with open(filename) as file:
            self.parameters = json.load(file)
            tasks_json = self.parameters.pop('tasks', None)

            for task_json in tasks_json:
                self.tasks_list.append(Task(task_json["id"],
                                            task_json["arrival"],
                                            task_json["size"],
                                            task_json["dt_max_const"],
                                            task_json["dt_max"],
                                            use_const))

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


def calculate_statistics(process_list: List[Task], round_opt=False, verbose=False):
    delay_time = 0.0
    response_time = 0.0
    done_in_time_count = 0
    process_count = len(process_list)

    for process in process_list:
        delay_time += process.get_delay_time()
        response_time += process.get_response_time()

        if process.is_done_in_time():
            done_in_time_count += 1

    if round_opt:
        avg_late = round(delay_time / process_count, 2)
        avg_latency = round(response_time / process_count, 2)
        done_in_time_percent = round(100 * done_in_time_count / process_count, 2)
    else:
        avg_late = delay_time / process_count
        avg_latency = response_time / process_count
        done_in_time_percent = 100 * done_in_time_count / process_count

    if verbose:
        print("Sredni_czas_opoznienia:", avg_late)
        print("Sredni_czas_odpowiedzi:", avg_latency)
        print("Zadania_obsluzone_w_czasie [%]:", done_in_time_percent)

    return avg_late, avg_latency, done_in_time_percent
