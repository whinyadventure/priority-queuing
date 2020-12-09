class Task:
    def __init__(self, process_id='0', start_time='0', duration='0', dt_max_const='0', dt_max='0', use_const=True):
        self.task_id = process_id
        self.arrival = float(start_time)
        self.size = float(duration)
        self.dt_max_const = float(dt_max_const)
        self.dt_max = float(dt_max)

        self.processed = 0.0
        self.processing_start = -1.0
        self.processing_end = -1.0
        self.max_starting_time = self.arrival + (self.dt_max_const if use_const else self.dt_max)
        self.max_end_time = self.arrival + self.size + (self.dt_max_const if use_const else self.dt_max)

    def to_string(self):
        return format(', '.join("%s: %s" % item for item in vars(self).items()))

    def is_done(self):
        return self.processed >= self.size-0.000000001

    # time exceeding (arrival + max_dt_const/max_dt)
    def get_delay_time(self):
        return max(self.processing_start - self.max_starting_time, 0)

    # total time spent in system
    def get_response_time(self):
        return self.processing_end - self.arrival

    def is_done_in_time(self):
        return self.processing_start <= self.max_starting_time

    def __lt__(self, other):
        return self.task_id < other.task_id
