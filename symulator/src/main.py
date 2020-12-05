from src.Algorithms import *

if __name__ == '__main__':
    alg_test = 2
    tests = range(1, 10)

    if alg_test is 0:
        print("BASIC FCFS")
    elif alg_test is 1:
        print("SUPER FCFS VER1:")
    else:
        print("SUPER FCFS VER2:")



    for i in tests:
        print("*#"*5, end=" ")
        file_path = "../res/res/tasks_cv-1-in-1000/"
        test_filename = "tasks_cv-1-wl-0."+str(i)+"-in-1000.txt"
        # test_filename = "test"+str(i)+".txt"
        print(test_filename)

        tasks = Tasks()
        tasks.read_input_file(file_path + test_filename)

        if alg_test is 0:
            basic_fcfs(tasks)
            #print(10 * "*", "\nSTATYSTYKI:")
            stats1 = calculate_statistics(tasks.tasks_list)
            tasks.clear()

        elif alg_test is 1:
            super_fcfs_vol1(tasks)
            #print(10 * "*", "\nSTATYSTYKI:")
            stats2 = calculate_statistics(tasks.tasks_list)
            tasks.clear()

        else:
            super_fcfs_vol2(tasks, 1)
            #print(10 * "*", "\nSTATYSTYKI:")
            stats3 = calculate_statistics(tasks.tasks_list)

        '''print("\n\n" + 20 * "#", "\nPorównanie wyników")
        print("\t" * 9,"BASIC FCFS:","\tSUPER FCFS VER1:","\tSUPER FCFS VER2:")
        print("Średnie odpóźnienie:", "\t" * 5,  stats1[0],"\t"*3,  stats2[0],"\t"*4, stats3[0])
        print("Średnia odpowiedź:", "\t" * 6,  stats1[1],"\t"*3,  stats2[1],"\t"*4,  stats3[1])
        print("Zadania obsłużone w czasie [%]:", "\t\t",  stats1[2],"\t"*3,  stats2[2],"\t"*4,  stats3[2])
        print("\n"*2)
        '''

