from src.Algorithms import *


def main():
    file_path = "../res/"
    # test_filename = "tasks_cv-1-wl-0.95.txt"
    test_filename = "example_input.txt"
    tasks = Tasks()
    tasks.read_input_file(file_path + test_filename)
    # tasks.print()



    opt = 0

    if opt in [1, 0]:
        print("\n" + 10 * "#", "\nFCFS:")
        basic_fcfs(tasks)
        print("\n" + 10 * "#", "\nSTATYSTYKI:")
        calculate_statistics(tasks.tasks_list)
    if opt in [2, 0]:
        print("\n" + 10 * "#", "\nSUPER FCFS:")
        super_fcfs(tasks)
        print("\n" + 10 * "#", "\nSTATYSTYKI:")
        calculate_statistics(tasks.tasks_list)


main()
