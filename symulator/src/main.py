from src.TestResults import *


def do_all_tests(cv_values, workload_values, interval_numbers, tests_no):
    files_number = len(cv_values) * len(workload_values) * len(interval_numbers) * tests_no
    current_file_number = 0
    test_res = TestsResults()
    for cv_value in cv_values:
        path = f'../res/cv-{cv_value}/'

        for workload_value in workload_values:
            for interval_number in interval_numbers:
                for test_number in range(tests_no):
                    # read file
                    file_path = f'{path}test-{test_number}/intervals-{interval_number}/'
                    test_filename = f'tasks_cv-{cv_value}-wl-0.{workload_value}-in-{interval_number}.txt'
                    file = file_path + test_filename
                    tasks = Tasks()
                    tasks.read_input_file(file, False)

                    # basic FCFS; algorithm_type = 0
                    basic_fcfs(tasks)
                    avg_late, avg_latency, done_in_time_percent = calculate_statistics(tasks.tasks_list)
                    test_res.append(Test(test_filename,
                                         cv_value,
                                         round(workload_value * 0.1, 1),
                                         interval_number,
                                         0,
                                         avg_late,
                                         avg_latency,
                                         done_in_time_percent))
                    tasks.clear()

                    # improved FCFS; algorithm_type = 1
                    enhanced_fcfs(tasks)
                    avg_late, avg_latency, done_in_time_percent = calculate_statistics(tasks.tasks_list)
                    test_res.append(Test(test_filename,
                                         cv_value,
                                         round(workload_value * 0.1, 1),
                                         interval_number,
                                         1,
                                         avg_late,
                                         avg_latency,
                                         done_in_time_percent))

                    tasks = Tasks()
                    tasks.read_input_file(file, True)

                    # basic FCFS; using dt_max_const; algorithm_type = 2
                    basic_fcfs(tasks)
                    avg_late, avg_latency, done_in_time_percent = calculate_statistics(tasks.tasks_list)
                    test_res.append(Test(test_filename,
                                         cv_value,
                                         round(workload_value * 0.1, 1),
                                         interval_number,
                                         2,
                                         avg_late,
                                         avg_latency,
                                         done_in_time_percent))
                    tasks.clear()

                    # improved FCFS; using dt_max_const; algorithm_type = 3
                    enhanced_fcfs(tasks)
                    avg_late, avg_latency, done_in_time_percent = calculate_statistics(tasks.tasks_list)
                    test_res.append(Test(test_filename,
                                         cv_value,
                                         round(workload_value * 0.1, 1),
                                         interval_number,
                                         3,
                                         avg_late,
                                         avg_latency,
                                         done_in_time_percent))

                    current_file_number += 1
                    print('\r\tProgress: [%d%%]' % (100 * current_file_number / files_number), end="")
    return test_res


if __name__ == '__main__':
    from_file = False
    test_results = None
    output_path = "../output/"
    if not from_file:
        cv_values = range(1, 11)
        workload_values = range(1, 10)
        interval_numbers = [1000]
        tests_no = 5
        test_res = do_all_tests(cv_values, workload_values, interval_numbers, tests_no)
        test_res.to_file(path=output_path)
    else:
        test_res = TestsResults()
        test_res.read_from_file("../output/output.txt")

    if test_res is not None:
        for cv in [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9, 10]
        ]:
            test_res.plot_results(show=True, to_file=True, output_path="../output/", const_param_values=cv, const_param="cv", x_var="wl")
        for wl in [
            [0.1, 0.2, 0.3],
            [0.4, 0.5, 0.6],
            [0.7, 0.8, 0.9]
        ]:
            test_res.plot_results(show=True, to_file=True, output_path="../output/", const_param_values=wl, const_param="wl", x_var="cv")
