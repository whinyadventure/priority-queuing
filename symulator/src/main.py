from src.Algorithms import *

if __name__ == '__main__':
    file_path = "../res/"
    # test_filename = "tasks_cv-1-wl-0.95.txt"
    test_filename = "example_input.txt"
    tasks = Tasks()
    tasks.read_input_file(file_path + test_filename)

    print("\n\n" + 20 * "#", "\nFCFS:")
    basic_fcfs(tasks)
    print(10 * "*", "\nSTATYSTYKI:")
    stats1 = calculate_statistics(tasks.tasks_list)
    tasks.clear()

    print("\n\n" + 20 * "#", "\nSUPER FCFS VER1:")
    super_fcfs(tasks)
    print(10 * "*", "\nSTATYSTYKI:")
    stats2 = calculate_statistics(tasks.tasks_list)

    print("\n\n" + 20 * "#", "\nSUPER FCFS VER2:")
    super_fcfs(tasks, 1)
    print(10 * "*", "\nSTATYSTYKI:")
    stats3 = calculate_statistics(tasks.tasks_list)

    print("\n\n" + 20 * "#", "\nPorównanie wyników")
    print("\t" * 9,"BASIC FCFS:","\tSUPER FCFS VER1:","\tSUPER FCFS VER2:")
    print("Średnie odpóźnienie:", "\t" * 5,  stats1[0],"\t"*3,  stats2[0],"\t"*4, stats3[0])
    print("Średnia odpowiedź:", "\t" * 6,  stats1[1],"\t"*3,  stats2[1],"\t"*4,  stats3[1])
    print("Zadania obsłużone w czasie [%]:", "\t\t",  stats1[2],"\t"*3,  stats2[2],"\t"*4,  stats3[2])
