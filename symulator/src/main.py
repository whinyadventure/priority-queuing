from src.Algorithms import *


def main():
    file_path = "../res/"
    test_filename = "tasks_cv-1-wl-0.95.txt"
    procs = Processes()
    procs.read_input_file(file_path + test_filename)
    procs.print()
    print("\n", 10 * "#", "\nFCFS:")
    basic_fcfs(procs)
    print("\n", 10 * "#", "\nSTATYSTYKI:")
    calculate_statistics(procs.process_list)


main()
