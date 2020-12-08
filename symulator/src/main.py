from src.TestResults import *


if __name__ == '__main__':
    test_res = TestsResults()
    alg_test = 2
    cv_values = [1]
    workload_values = range(1, 10)
    interval_numbers = [100, 1000]  # [10, 100, 1000]
    tests_no = 5
    results = []
    files_number = len(cv_values) * len(workload_values) * len(interval_numbers) * tests_no
    current_file_number = 0
    for cv_value in cv_values:
        path = "../res/cv-"+str(cv_value)+"/"
        for workload_value in workload_values:
            for interval_number in interval_numbers:
                for test_number in range(tests_no):
                    # read file
                    file_path = path + "test-" + str(test_number) + "/intervals-" + str(interval_number) + "/"
                    test_filename = "tasks_cv-1-wl-0." + str(workload_value) + "-in-" + str(interval_number) + ".txt"
                    file = file_path+test_filename
                    tasks = Tasks()
                    tasks.read_input_file(file)

                    # basic FCFS
                    basic_fcfs(tasks)
                    avg_late, avg_latency, done_in_time_percent = calculate_statistics(tasks.tasks_list)
                    test_res.append(Test(test_filename, cv_value, workload_value*0.1, interval_number, 0, avg_late, avg_latency, done_in_time_percent))
                    tasks.clear()

                    # improved FCFS
                    super_fcfs_vol1(tasks)
                    avg_late, avg_latency, done_in_time_percent = calculate_statistics(tasks.tasks_list)
                    test_res.append(Test(test_filename, cv_value, workload_value*0.1, interval_number, 1, avg_late, avg_latency, done_in_time_percent))

                    current_file_number += 1
                    print('\r\tProgress: [%d%%]' % (100 * current_file_number / files_number), end="")

    #test_res.print_all()
    #test_res.to_file()
    test_res.plot_results(output_path="../output/", show=True, to_file=False)
    test_res.plot_differences(output_path="../output/", show=True, to_file=False)