class Task(object):
    def __init__(self, process_id="0", start_time="0", duration="0", dt_max="0"):
        self.task_id = process_id
        self.arrival = float(start_time)
        self.size = float(duration)
        self.processed = 0.0
        self.dt_max = float(dt_max)
        self.processing_start = -1.0
        self._processing_end = -1.0
        self.max_end_time = self.arrival + self.size + self.dt_max

    def to_string(self):
        attrs = vars(self)
        return format(', '.join("%s: %s" % item for item in attrs.items()))

    @property
    def processing_end(self):
        return self._processing_end

    @processing_end.setter
    def processing_end(self, value):
        self._processing_end = value
        self.processed = round(self.processing_end - self.processing_start, 2)

    def is_done(self):
        return self.processing_start + self.processed >= self.size

    # czas opoznienia
    def get_waiting_time(self):
        return self.arrival + self.processing_start

    # czas odpowiedzi
    def get_turn_around_time(self):
        return self.arrival + self.processing_start + self.processing_end

    def is_done_in_time(self):
        return self.processing_end <= self.arrival + self.size + self.dt_max
