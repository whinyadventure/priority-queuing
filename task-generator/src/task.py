class Task:
    def __init__(self, task_id, arrival, size=None, dt_max=None):
        self.id = task_id
        self.arrival = arrival
        self.size = size
        self.dt_max = dt_max      # maximum tolerable delay


