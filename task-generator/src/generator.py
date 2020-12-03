import numpy as np
from scipy.stats import skewnorm
import matplotlib.pyplot as plt
import json

from src.constants import *
from src.task import *


class Generator(object):
    def __init__(self, c_var, workload):  # coefficient of variation, system workload
        self.c_var = c_var
        self.workload = workload
        self.bimodal = None
        self.intervals = []  # number of tasks in consecutive time intervals
        self.tasks = []  # list of tasks arranged chronologically
        self.sizes = []

    # TODO: concatenation of two normal distributions or erlang and normal distributions
    #       tuning distribution input arguments to get expected value of coefficient of variation

    def populate_intervals(self):

        if self.c_var == 1:
            mean_1 = 5
            std_1 = 10
            size_1 = 0.5 * N_SAMPLES

            mean_2 = 5
            std_2 = 45
            size_2 = N_SAMPLES - size_1

            norm_1 = np.random.normal(mean_1, std_1, int(size_1))
            norm_2 = np.random.normal(mean_2, std_2, int(size_2))

            bimodal = np.concatenate([norm_1, norm_2])
            self.bimodal = np.intc((np.round(bimodal[bimodal > 1])))
        else:
            pass

        self.intervals = np.random.choice(self.bimodal, INTERVALS)

    def draw_arrival_times(self):
        current_id = 1
        duplicates = []

        for idx, val in enumerate(self.intervals):
            arrivals = np.round(np.random.exponential(size=val) * 0.1, 8)
            arrivals.sort()

            duplicates.append(len(arrivals) == len(set(arrivals)))

            for i in range(val):
                self.tasks.append(Task(current_id, arrivals[i] + idx))
                current_id += 1

        print(f'arrivals: {all(duplicates)}')

    def draw_sizes(self):  # mean size of tasks = system workload / mean nbr of tasks per interval
        mean_nbr = np.mean(self.intervals)
        mean_size = self.workload / mean_nbr
        self.sizes = np.random.normal(mean_size, mean_size * 0.1, sum(self.intervals))  # max/min approx 2

        for idx, val in enumerate(self.sizes):
            self.tasks[idx].size = val

    def draw_dts_max(self, same=True):
        mean_size = np.mean(self.sizes)
        dt_max = np.random.normal(mean_size, mean_size * 0.25)  # minimize probability of negative value -> 4 * std_dev

        for task in self.tasks:
            task.dt_max = dt_max

            if not same:
                dt_max = np.random.normal(mean_size, mean_size * 0.25)

    def save_to_file(self):
        directory = 'res/'
        # cv - coefficient of variation, wl - system workload, in - nbr of intervals
        filename = f'tasks_cv-{self.c_var}-wl-{self.workload}-in-{len(self.intervals)}.txt'
        path = directory + filename

        with open(path, "w") as file:
            content = {'c_var': np.std(self.intervals) / np.mean(self.intervals),
                       'workload': np.mean(self.intervals) * np.mean(self.sizes),
                       'intervals_n': len(self.intervals),
                       'columns': 'id arrival size dt_max',
                       'tasks': [ob.__dict__ for ob in self.tasks]}

            json.dump(content, file, indent=2)

    @staticmethod
    def load_from_file(path='res/tasks_cv-1-wl-0.95.txt'):
        with open(path) as json_file:
            data = json.load(json_file)
            c_var, workload, cols = data['c_var'], data['workload'], data['columns']
            cols = cols.split()

            return [Task(item[cols[0]], item[cols[1]], item[cols[2]], item[cols[3]]) for item in data['tasks']]

    def print_intervals(self):
        print(f'\nGENERATED INTERVALS')
        print(f'c_var: {np.std(self.intervals) / np.mean(self.intervals)}\n')
        print('\n'.join(f'[{idx}-{idx + 1}]: {val}' for idx, val in enumerate(self.intervals)))

    def sizes_stats(self):
        print(f'\nGENERATED TASK SIZES STATISTICS')
        print(f'min: {min(self.sizes)}')
        print(f'max: {max(self.sizes)}')
        print(f'max/min: {max(self.sizes) / min(self.sizes)}')
        print(f'mean: {np.mean(self.sizes)}')
        print(f'sum: {sum(self.sizes)}')

    def dt_max_stats(self):
        min_dt_max = min(self.tasks, key=lambda task: task.dt_max).dt_max
        max_dt_max = max(self.tasks, key=lambda task: task.dt_max).dt_max

        print(f'\nGENERATED TASK MAXIMUM TOLERABLE DELAY STATISTICS')
        print(f'min: {min_dt_max}')
        print(f'max: {max_dt_max}')
        print(f'mean: {np.mean([task.dt_max for task in self.tasks])}')
        print(f'std dev: {np.std([task.dt_max for task in self.tasks])}')
        print(f'sum: {np.sum([task.dt_max for task in self.tasks])}')

    def print_tasks(self):
        print(f'\nGENERATED TASKS')

        for task in self.tasks:
            print(f'id: {task.id} arrival time: {task.arrival} size: {task.size} dt_max: {task.dt_max}')

    def plot_bimodal(self):
        plt.hist(self.bimodal, N_BINS, density=True)
        plt.show()
