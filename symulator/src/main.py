from src.Algorithms import *


class Test(object):
    def __init__(self, filename, cv, wl, interval_number, alg_type, avg_late, avg_latency, done_in_time_percent):
        self.interval_number = interval_number
        self.cv = cv
        self.wl = wl
        self.alg_type = alg_type
        self.avg_late = avg_late
        self.avg_latency = avg_latency
        self.done_in_time_percent = done_in_time_percent
        self.filename = filename


    def to_string(self):
        attrs = vars(self)
        return format(', '.join("%s: %s" % item for item in attrs.items()))
    
class TestsResults():
    test_list: List[Test]

    def __init__(self):
        self.test_list = []

    def append(self, test_result):
        self.test_list.append(test_result)

    def print_all(self):
        for test in self.test_list:
            print(test.to_string())


if __name__ == '__main__':
    alg_test = 2
    cv_values = [1]
    workload_values = range(1, 10)
    interval_numbers = (10, 100, 1000)
    test_res = TestsResults()
    results = []
    files_number = len(cv_values) * len(workload_values) * len(interval_numbers)
    current_file_number = 0
    for cv_value in cv_values:
        for workload_value in workload_values:
            for interval_number in interval_numbers:
                # read file
                file_path = "../res/res/tasks_cv-1-in-"+str(interval_number)+"/"
                test_filename = "tasks_cv-1-wl-0." + str(workload_value) + "-in-" + str(interval_number) + ".txt"
                tasks = Tasks()
                tasks.read_input_file(file_path + test_filename)

                # basic FCFS
                basic_fcfs(tasks)
                avg_late, avg_latency, done_in_time_percent = calculate_statistics(tasks.tasks_list)
                test_res.append(Test(test_filename, cv_value, workload_value, interval_number, 0, avg_late, avg_latency, done_in_time_percent))
                tasks.clear()

                # improved FCFS
                super_fcfs_vol1(tasks)
                avg_late, avg_latency, done_in_time_percent = calculate_statistics(tasks.tasks_list)
                test_res.append(Test(test_filename, cv_value, workload_value, interval_number, 1, avg_late, avg_latency, done_in_time_percent))

                current_file_number += 1
                print('\r\tProgress: [%d%%]' % (100 * current_file_number / files_number), end="")

    test_res.print_all()