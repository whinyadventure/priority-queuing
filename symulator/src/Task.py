# todo remove round(...,2)


class Task(object):
    def __init__(self, process_id="0", start_time="0", duration="0", dt_max="0"):
        self.task_id = process_id
        self.arrival = float(start_time)
        self.size = float(duration)
        self.processed = 0.0
        self.dt_max = float(dt_max)
        self.processing_start = -1.0
        self.processing_end = -1.0
        self.max_starting_time = self.arrival + self.dt_max
        self.max_end_time = self.arrival + self.size + self.dt_max

    def to_string(self):
        self.arrival = round(self.arrival, 2)
        self.size = round(self.size, 2)
        self.dt_max = round(self.dt_max, 2)
        self.processed = round(self.processed, 2)
        self.processing_start = round(self.processing_start, 2)
        self.processing_end = round(self.processing_end, 2)
        attrs = vars(self)
        return format(', '.join("%s: %s" % item for item in attrs.items()))

    def is_done(self):
        return self.processed >= self.size

    # czas opoznienia
    def get_waiting_time(self):
        return self.arrival + self.processing_start

    # czas odpowiedzi
    def get_turn_around_time(self):
        return self.arrival + self.processing_start + self.processing_end

    def is_done_in_time(self):
        return self.processing_end <= self.arrival + self.size + self.dt_max
