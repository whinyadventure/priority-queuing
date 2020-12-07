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
                for wl in np.linspace(0.1, 0.9, num=9):
                    gen = Generator(cv, np.round(wl, 1))
                    gen.generate_log(directory, itr)


if __name__ == '__main__':
    # gen = Generator(sys.argv[1], sys.argv[2])

    generate_log_batch(1, N_TESTS)  # coefficient of variance, number of tests





