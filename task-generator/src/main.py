import os
import numpy as np

from src.generator import *


def generate_log_batch(cv, test_nbr):
    for idx in range(test_nbr):
        for itr in INTERVAL_NBR:
            directory = f'res/cv-{cv}/test-{idx}/intervals-{itr}/'

            try:
                os.makedirs(directory)
            except OSError:
                print("Creation of the directory %s failed" % directory)
            else:
                for wl in range(1, 10):
                    gen = Generator(cv, np.round(wl * 0.1, 1))
                    gen.generate_log(directory, itr)


if __name__ == '__main__':
    # gen = Generator(sys.argv[1], sys.argv[2])

    generate_log_batch(1, N_TESTS)  # coefficient of variance, number of tests

    '''
    gen = Generator(1, 0.1)
    gen.populate_intervals(1000)
    gen.intervals_stats()
    gen.draw_arrival_times()
    gen.are_arrivals_unique()
    gen.draw_sizes()
    gen.sizes_stats()
    gen.draw_dts_max()
    gen.dt_max_stats()
    gen.save_to_file('res/')
    #gen.print_tasks()
    '''




