class Task:
    def __init__(self, task_id, arrival, size=None, dt_max_const=None, dt_max=None):
        self.id = task_id
        self.arrival = arrival
        self.size = size
        self.dt_max_const = dt_max_const      # same maximum tolerable delay for all
        self.dt_max = dt_max                  # unique maximum tolerable delay for each
