import time


class Runtime:
    def __init__(self, start_time:float):
        self.start_time = start_time
        self.base_runtime = self.get_runtime()
        self._runtime_minutes = None
        self._runtime_hours = None

    def get_runtime(self):
        end_time = time.time()
        return round((end_time - self.start_time), 3)

    @property
    def runtime_minutes(self):
        self._runtime_minutes = round(self.base_runtime / 60, 3)
        return self._runtime_minutes

    @property
    def runtime_hours(self):
        self._runtime_hours = round(self.base_runtime / 60 / 60, 3)
        return self._runtime_hours
