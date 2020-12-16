import os
import sys
import numpy as np

from src.generator import *


def generate_log_batch():
    for cv in range(1, 11):  # for coefficient of variation in range 1:10
        for idx in range(N_TESTS):
            for itr in INTERVAL_NBR:
                directory = f'res/cv-{cv}/test-{idx}/intervals-{itr}/'

                if not os.path.exists(directory):
                    try:
                        os.makedirs(directory)
                    except OSError:
                        print("Creation of the directory %s failed" % directory)
                        sys.exit(1)

                for wl in range(1, 10):
                    gen = Generator(cv, np.round(wl * 0.1, 1))
                    gen.generate_log(directory, itr)


if __name__ == '__main__':
    generate_log_batch()




