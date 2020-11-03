from src.Algorithms import *


def main():
    file_path = "../res/"
    test_filename = "tasks_cv-1-wl-0.95.txt"
    tasks = Tasks()
    tasks.read_input_file(file_path + test_filename)
    tasks.print()
    print("\n", 10 * "#", "\nFCFS:")
    basic_fcfs(tasks)
    print("\n", 10 * "#", "\nSTATYSTYKI:")
    calculate_statistics(tasks.tasks_list)


main()
