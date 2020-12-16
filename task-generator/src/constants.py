import numpy as np

INTERVAL_NBR = [1000]
N_TESTS = 5
N_SAMPLES = 50000
N_BINS = 50

MEAN_1 = 3
STD_1 = 1

PARAMS = np.array([[0.3, 6, 22],    # [size_1_multiplier, mean_2, std_2]
                   [0.67, 9, 65],
                   [0.83, 15, 140],
                   [0.89, 21, 270],
                   [0.92, 30, 490],
                   [0.945, 39, 710],
                   [0.9553, 48, 1060],
                   [0.9655, 51, 1410],
                   [0.973, 75, 1680],
                   [0.9785, 94, 2010]])
