import sys

from src.generator import *

if __name__ == '__main__':
    # gen = Generator(sys.argv[1], sys.argv[2])

    gen = Generator(1, 0.95)
    gen.populate_intervals()
    gen.get_arrival_time()
    gen.get_size()
    gen.get_dt_max()
    gen.print_tasks()
    gen.sizes_stats()
    gen.dt_max_stats()
    gen.save_to_file()
    # gen.load_from_file()





