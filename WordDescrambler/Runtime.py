import time
from datetime import timedelta

class Runtime:
    def __init__(self, start_time:float):
        self.start_time = start_time
        self._runtime = None
        self._runtime_seconds = None
        self._runtime_minutes = None
        self._runtime_hours = None
        self._runtime_string = None
        self._runtime_string_suffix = None
        self._runtime_timedelta:timedelta or None = None

    def __str__(self):
        return self.runtime_timedelta #self.runtime_string

    @property
    def runtime_timedelta(self):
        self._runtime_timedelta = str(timedelta(seconds=self.runtime_seconds))
        return self._runtime_timedelta

    @property
    def runtime_string(self):
        self._runtime_string = f"Program runtime was {self.runtime} {self._runtime_string_suffix}."
        return self._runtime_string

    # TODO: have this return a dict of 'number', 'resolution' instead of using string suffix?
    @property
    def runtime(self):
        if 60 < self.runtime_seconds < 3600:
            self._runtime = self.runtime_minutes
            self._runtime_string_suffix = 'minutes'
        elif self.runtime_seconds > 3600:
            self._runtime = self.runtime_hours
            self._runtime_string_suffix = 'hours'
        else:
            self._runtime = self.runtime_seconds
            self._runtime_string_suffix = 'seconds'
        return self._runtime
    
    @property
    def runtime_seconds(self):
        end_time = time.time()
        self._runtime_seconds =  round((end_time - self.start_time), 3)
        return self._runtime_seconds

    @property
    def runtime_minutes(self):
        self._runtime_minutes = (self.runtime_seconds / 60)
        if self._runtime_minutes <= 1:
            self._runtime_minutes = round(self._runtime_minutes, 3)
        else:
            self._runtime_minutes = round(self._runtime_minutes, 2)
        return self._runtime_minutes

    @property
    def runtime_hours(self):
        self._runtime_hours = (self.runtime_seconds / 60 / 60)
        if self._runtime_hours <= 1:
            self._runtime_hours = round(self._runtime_hours, 3)
        else:
            self._runtime_hours = round(self._runtime_hours, 2)
        return self._runtime_hours
