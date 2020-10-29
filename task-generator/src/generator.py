import numpy as np
import matplotlib.pyplot as plt
import json

from src.constants import *
from src.task import *


class Generator(object):
    def __init__(self, c_var, workload):     # coefficient of variation, system workload
        self.c_var = c_var
        self.workload = workload
        self.intervals = []     # number of tasks in consecutive time intervals
        self.tasks = []     # list of tasks arranged chronologically
        self.sizes = []

    # TODO: concatenation of two normal distributions or erlang and normal distributions
    #       tuning distribution input arguments to get expected value of coefficient of variation

    def populate_intervals(self):
        '''
        mu_1 = np.random.randint(MIN_INIT_MEAN, MAX_INIT_MEAN)
        sigma_1 = mu_1 * self.c_var     # c_var = std_dev / mean

        mu_2 = mu_1 * self.c_var ** 2
        sigma_2 = sigma_1 * (1 + 0.1 * self.c_var)

        dist_1 = np.random.normal(mu_1, sigma_1, N_SAMPLES)
        dist_2 = np.random.normal(mu_2, sigma_2, N_SAMPLES)

        bimodal_dist = np.concatenate([dist_1, dist_2])

        self.intervals = random.choices(bimodal_dist, k=INTERVALS)
        '''

        # self.intervals = [3, 3, 4, 7, 8]
        self.intervals = np.random.randint(0, 5, 5)

    def get_arrival_time(self):
        current_id = 1

        for idx, val in enumerate(self.intervals):
            arrivals = np.random.exponential(size=val) * 0.1
            arrivals.sort()

            for i in range(val):
                self.tasks.append(Task(current_id, arrivals[i] + idx))
                current_id += 1

    def get_size(self):     # mean size of tasks = system workload / mean nbr of tasks per interval
        mean_nbr = np.mean(self.intervals)
        mean_size = self.workload / mean_nbr
        self.sizes = np.random.normal(mean_size, mean_size*0.1, sum(self.intervals))    # max/min approx 2

        for idx, val in enumerate(self.sizes):
            self.tasks[idx].size = val

    def get_dt_max(self, same=True):
        mean_size = np.mean(self.sizes)
        dt_max = np.random.normal(mean_size, mean_size*0.25)    # minimize probability of negative value -> 4 * std_dev

        for task in self.tasks:
            task.dt_max = dt_max

            if not same:
                dt_max = np.random.normal(mean_size, mean_size*0.25)

    def save_to_file(self):
        directory = 'res/'
        filename = f'tasks_cv-{self.c_var}-wl-{self.workload}.txt'
        path = directory + filename

        with open(path, "w") as file:
            content = {'c_var': self.c_var,
                        'workload': self.workload,
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

    # TODO: plotting as hist generated bimodal distribution
    def plot_bimodal(self):
        pass
