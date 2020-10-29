import json
from typing import List


class Process(object):
    def __init__(self, process_id="0", start_time="0", duration="0", dt_max="0"):
        self.process_id = process_id
        self.start_time = float(start_time)
        self.duration = float(duration)
        self.processed = 0.0
        self.dt_max = float(dt_max)
        self.processing_start = -1.0
        self._processing_end = -1.0
        self.max_end_time = self.start_time+self.duration+self.dt_max

    def to_string(self):
        attrs = vars(self)
        return format(', '.join("%s: %s" % item for item in attrs.items()))

    @property
    def processing_end(self):
        return self._processing_end

    @processing_end.setter
    def processing_end(self, value):
        self._processing_end = value
        self.processed = round(self.processing_end - self.processing_start, 2)

    def is_done(self):
        return self.processing_start + self.processed >= self.duration

    #czas opoznienia
    def get_waiting_time(self):
        return self.start_time+self.processing_start

    #czas odpowiedzi
    def get_turn_around_time(self):
        return self.start_time+self.processing_start+self.processing_end

    def is_done_in_time(self):
        return self.processing_end <= self.start_time+self.duration+self.dt_max

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
            self.parameters = self.parse_parameters(data[0])
            for line in data[1:]:
                parsed_line = self.parse_line(line[:-1])
                self.process_list.append(Process(*parsed_line))

    def print(self):
        print("PARAMETERS: ", end="")
        for key, value in self.parameters.items():
            print(key, ":", value, end=" ")
        print("\nProcess list:")
        for proc in self.process_list:
            print(proc.to_string())


class Event(object):
    def __init__(self, time, process_id):
        self.time = time
        self.process_id = process_id


def calculate_statistics(process_list : List[Process], file=False, filename="stats.txt"):
    waiting_time = 0.0 # czas opoznienia
    turn_around_time = 0.0 # czas odpowiedz
    done_in_time_count = 0
    for process in process_list:
        waiting_time += process.get_waiting_time()
        turn_around_time += process.get_turn_around_time()
        if process.is_done_in_time():
            done_in_time_count+=1
    process_count = len(process_list)
    print("Sredni czas opoznienia:", round(waiting_time/process_count,2))
    print("Sredni czas odpowiedzi:", round(turn_around_time / process_count, 2))
    print("Zadania obsluzone w czasie [%]:", round(100*done_in_time_count/ process_count, 2))



# zakladam, ze zadania otrzymane z generatora sa posortowane zgodnie z czasem pojawienia sie w systemie
def basic_fcfs(processes: Processes):
    events = []
    process_list = processes.process_list
    time = process_list[0].start_time
    delay = 0
    for proc in process_list:
        time += delay
        events.append(Event(time, proc.process_id))
        proc.processing_start = time
        proc.processing_end = time + proc.duration
        delay = proc.duration

    print("EVENTS:\nprocess_id processing_start")
    for ev in events:
        print(ev.process_id, ev.time)
    print()
    processes.print()


def main():
    procs = Processes()
    procs.read_input_file("../res/example_input.txt")
    procs.print()
    print("\n", 10 * "#", "\nFCFS:")
    basic_fcfs(procs)
    print("\n", 10 * "#", "\nSTATYSTYKI:")
    calculate_statistics(procs.process_list)


main()
