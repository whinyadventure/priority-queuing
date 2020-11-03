import json
from typing import List

from src.Process import *


class Processes(object):
    process_list: List[Process]

    def __init__(self):
        self.process_list = []
        self.parameters = dict()

    @staticmethod
    def parse_line(line):
        return line.split(" ")

    @staticmethod
    def parse_parameters(line):
        return json.loads(line)

    def read_input_file(self, filename="input.txt"):
        with open(filename) as file:
            data = file.readlines()
            # parse json

    def print(self):
        print("PARAMETERS: ", end="")
        for key, value in self.parameters.items():
            print(key, ":", value, end=" ")
        print("\nProcess list:")
        for proc in self.process_list:
            print(proc.to_string())


def calculate_statistics(process_list: List[Process], file=False, filename="stats.txt"):
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
