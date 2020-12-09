from src.TestResults import *


if __name__ == '__main__':

    cv_values = [1]
    workload_values = range(1, 10)
    interval_numbers = [100, 1000]  # [10, 100, 1000]
    tests_no = 5
    results = []
    files_number = len(cv_values) * len(workload_values) * len(interval_numbers) * tests_no
    current_file_number = 0
    test_res = TestsResults(interval_numbers)
    
    for cv_value in cv_values:
        path = f'../res/cv-{cv_value}/'
        
        for workload_value in workload_values:
            for interval_number in interval_numbers:
                for test_number in range(tests_no):
                    # read file
                    file_path = f'{path}test-{test_number}/intervals-{interval_number}/'
                    test_filename = f'tasks_cv-1-wl-0.{workload_value}-in-{interval_number}.txt'
                    file = file_path + test_filename
                    tasks = Tasks()
                    tasks.read_input_file(file)

                    # basic FCFS; algorithm_type = 0
                    basic_fcfs(tasks)
                    avg_late, avg_latency, done_in_time_percent = calculate_statistics(tasks.tasks_list)
                    test_res.append(Test(test_filename,
                                         cv_value,
                                         workload_value * 0.1,
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
                                         workload_value * 0.1,
                                         interval_number,
                                         1,
                                         avg_late,
                                         avg_latency,
                                         done_in_time_percent))

                    current_file_number += 1
                    
                    print('\r\tProgress: [%d%%]' % (100 * current_file_number / files_number), end="")

    '''
    test_res = TestsResults(4)

    #file = '../res/example_input_separate.txt'
    #file = '../res/example_input_overlaying.txt'
    #file = '../res/example_input_pq.txt'
    file = '../res/example_input_pq_idle.txt'
    tasks = Tasks()
    tasks.read_input_file(file)
    basic_fcfs(tasks)
    avg_late, avg_latency, done_in_time_percent = calculate_statistics(tasks.tasks_list)
    test_res.append(Test(file, 1, 0.95, 4, 0, avg_late, avg_latency, done_in_time_percent))

    tasks.clear()

    enhanced_fcfs(tasks)
    avg_late, avg_latency, done_in_time_percent = calculate_statistics(tasks.tasks_list)
    test_res.append(Test(file, 1, 0.95, 5, 1, avg_late, avg_latency, done_in_time_percent))
    '''

    test_res.print_all()
    test_res.to_file(path="../output/")
    test_res.plot_results(output_path="../output/", show=False, to_file=True)
    test_res.plot_differences(output_path="../output/", show=False, to_file=True)
