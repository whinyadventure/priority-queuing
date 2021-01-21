import numpy as np
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

    def populate_intervals(self, interval_nbr):
        if self.c_var == 0.3:
            mean_1 = 13
            std_1 = 13
            size_1 = 0.2 * N_SAMPLES

            mean_2 = 13
            std_2 = 0.5
        elif self.c_var == 0.7:
            mean_1 = 6
            std_1 = 6
            size_1 = 0.4 * N_SAMPLES

            mean_2 = 13
            std_2 = 13
        else:
            mean_1 = 3
            std_1 = 1
            size_1 = PARAMS_CV_1_TO_10[self.c_var - 1][0] * N_SAMPLES

            mean_2 = PARAMS_CV_1_TO_10[self.c_var - 1][1]
            std_2 = PARAMS_CV_1_TO_10[self.c_var - 1][2]

        size_2 = N_SAMPLES - size_1

        norm_1 = np.random.normal(mean_1, std_1, int(size_1))
        norm_2 = np.random.normal(mean_2, std_2, int(size_2))

        bimodal = np.concatenate([norm_1, norm_2])
        self.bimodal = np.intc((np.round(bimodal[bimodal > 1])))

        self.intervals = np.random.choice(self.bimodal, interval_nbr)

    def draw_arrival_times(self):
        current_id = 1

        for idx, val in enumerate(self.intervals):
            arrivals = (np.random.exponential(size=val) * 0.1) + idx
            arrivals.sort()
            # print(f'idx: {idx} val: {val} arrivals: {arrivals}\n')

            for i in range(val):
                self.tasks.append(Task(current_id, arrivals[i]))
                current_id += 1

    @staticmethod
    def drop_negative(mean, multiplier, out_size):
        output = 0

        while np.min(output) <= 0:
            output = np.random.normal(mean, mean * multiplier, out_size)

        return output if len(output) > 1 else float(output)

    def draw_sizes(self):  # mean size of tasks = system workload / mean nbr of tasks per interval
        mean_nbr = np.mean(self.intervals)
        mean_size = self.workload / mean_nbr
        # max/min approx 2 +- 0.5
        self.sizes = self.drop_negative(mean=mean_size, multiplier=0.1, out_size=sum(self.intervals))

        for idx, val in enumerate(self.sizes):
            self.tasks[idx].size = val

    def draw_dts_max(self):
        mean_size = np.mean(self.sizes)
        # minimize probability of negative value -> 4 * std_dev
        dt_max_const = self.drop_negative(mean=mean_size, multiplier=0.25, out_size=1)

        for task in self.tasks:
            task.dt_max_const = dt_max_const
            task.dt_max = self.drop_negative(mean=mean_size, multiplier=0.25, out_size=1)

    def save_to_file(self, directory):
        # cv - coefficient of variation, wl - system workload, in - nbr of intervals
        filename = f'tasks_cv-{self.c_var}-wl-{self.workload}-in-{len(self.intervals)}.txt'
        path = directory + filename

        with open(path, "w") as file:
            content = {'c_var': np.std(self.intervals) / np.mean(self.intervals),
                       'workload': np.mean(self.intervals) * np.mean(self.sizes),
                       'intervals_n': len(self.intervals),
                       'columns': 'id arrival size dt_max_const dt_max',
                       'tasks': [ob.__dict__ for ob in self.tasks]}

            json.dump(content, file, indent=2)

    def generate_log(self, directory, interval_nbr):
        self.populate_intervals(interval_nbr)
        self.draw_arrival_times()
        self.draw_sizes()
        self.draw_dts_max()
        self.save_to_file(directory)

    @staticmethod
    def load_from_file(path='res/cv-1/test-0/intervals-1000/tasks_cv-1-wl-0.1-in-1000.txt'):
        with open(path) as json_file:
            data = json.load(json_file)
            c_var, workload, intervals_n, cols = data['c_var'], data['workload'], data['intervals_n'], data['columns']
            cols = cols.split()

            return [Task(item[cols[0]],
                         item[cols[1]],
                         item[cols[2]],
                         item[cols[3]],
                         item[cols[4]]) for item in data['tasks']]

    # helper functions
    def bimodal_stats(self):
        print(f'\nGENERATED BIMODAL DISTRIBUTION STATISTICS')
        print(f'size: {len(self.bimodal)}')
        print(f'min: {min(self.bimodal)}')
        print(f'max: {max(self.bimodal)}')
        print(f'mean: {np.mean(self.bimodal)}')
        print(f'std dev: {np.std(self.bimodal)}')
        print(f'c_var: {np.std(self.bimodal) / np.mean(self.bimodal)}')

    def intervals_stats(self):
        print(f'\nGENERATED INTERVALS STATISTICS')
        print(f'c_var: {np.std(self.intervals) / np.mean(self.intervals)}')
        print(f'mean: {np.mean(self.intervals)}')
        print(f'std dev: {np.std(self.intervals)}')

    def print_intervals(self):
        print(f'\nGENERATED INTERVALS')
        print(''.join(f'[{idx}-{idx + 1}]: {val}' for idx, val in enumerate(self.intervals)))

    def are_arrivals_unique(self):
        arrivals = [task.arrival for task in self.tasks]

        return print('\nARRIVALS UNIQUE: TRUE') if len(arrivals) == len(set(arrivals)) \
            else print('\nARRIVALS UNIQUE: FALSE')

    def sizes_stats(self):
        print(f'\nGENERATED TASK SIZES STATISTICS')
        print(f'min: {min(self.sizes)}')
        print(f'max: {max(self.sizes)}')
        print(f'max/min: {max(self.sizes) / min(self.sizes)}')
        print(f'mean: {np.mean(self.sizes)}')
        print(f'sum: {sum(self.sizes)}')
        print(f'workload: {np.mean(self.sizes) * np.mean(self.intervals)}')

    def dt_max_stats(self):
        min_dt_max = min(self.tasks, key=lambda task: task.dt_max).dt_max
        max_dt_max = max(self.tasks, key=lambda task: task.dt_max).dt_max

        print(f'\nGENERATED TASK MAXIMUM TOLERABLE DELAY STATISTICS')
        print(f'dt_max_const: {self.tasks[0].dt_max_const}')
        print(f'min: {min_dt_max}')
        print(f'max: {max_dt_max}')
        print(f'mean: {np.mean([task.dt_max for task in self.tasks])}')
        print(f'std dev: {np.std([task.dt_max for task in self.tasks])}')
        print(f'sum: {np.sum([task.dt_max for task in self.tasks])}')

    def print_tasks(self):
        print(f'\nGENERATED TASKS')

        for task in self.tasks:
            print(f'id: {task.id} arrival time: {task.arrival} size: {task.size} dt_max_const: {task.dt_max_const} '
                  f'dt_max: {task.dt_max}')

    def plot_bimodal(self):
        plt.hist(self.bimodal, N_BINS, density=True)
        plt.show()
