import time
from datetime import timedelta, datetime
from pathlib import Path

class Runtime:
    """
    This module contains the `Runtime` class which can be used to measure the runtime of a program.

    The `Runtime` class has the following attributes:
        - `start_time`: The starting time of the program. It is a float representing the number of seconds since the epoch.
        - `_runtime`: The calculated runtime of the program.
        - `_runtime_seconds`: The runtime of the program in seconds.
        - `_runtime_minutes`: The runtime of the program in minutes.
        - `_runtime_hours`: The runtime of the program in hours.
        - `_runtime_string`: A string representation of the runtime.
        - `_runtime_string_suffix`: The string suffix representing the unit of measurement for the runtime.
        - `_runtime_timedelta`: A `timedelta` object representing the runtime.
        - `_use_timedelta`: A boolean indicating whether to use `timedelta` for representing the runtime.

    The `Runtime` class has the following methods:
        - `__init__(self, start_time:float, use_timedelta=False)`: Initializes a new `Runtime` object with the given start time and an optional flag indicating whether to use `timedelta` for representing the runtime.
        - `__str__(self)`: Returns a string representation of the `Runtime` object.
        - `runtime_timedelta(self)`: Calculates and returns the runtime as a `timedelta` object.
        - `runtime_string(self)`: Generates a string representation of the runtime.
        - `runtime(self)`: Calculates and returns the runtime in the appropriate format based on the value of `_use_timedelta`.
        - `runtime_seconds(self)`: Calculates and returns the runtime in seconds.
        - `runtime_minutes(self)`: Calculates and returns the runtime in minutes.
        - `runtime_hours(self)`: Calculates and returns the runtime in hours.

    Example usage:
    ```python
    # Create a Runtime object with a start time of 1626778400.0 seconds (July 20, 2021 12:00:00 AM)
    rt = Runtime(1626778400.0)

    # Get the string representation of the Runtime object
    print(str(rt))  # Output: "Runtime timer: started on Tue Jul 20 00:00:00 2021."

    # Get the runtime as a timedelta object
    timedelta = rt.runtime_timedelta()

    # Get the string representation of the runtime
    string = rt.runtime_string()

    # Get the runtime in the appropriate format
    runtime = rt.runtime()

    # Get the runtime in seconds
    seconds = rt.runtime_seconds()

    # Get the runtime in minutes
    minutes = rt.runtime_minutes()

    # Get the runtime in hours
    hours = rt.runtime_hours()
    ```
    """
    def __init__(self, start_time:float, use_timedelta=False):
        self.start_time = start_time
        self._runtime = None
        self._runtime_seconds = None
        self._runtime_minutes = None
        self._runtime_hours = None
        self._runtime_string = None
        self._runtime_string_suffix = None
        self._runtime_timedelta:timedelta or None = None
        self._use_timedelta: bool = use_timedelta

    def __str__(self):
        return f"Runtime timer: started on {self.pretty_start_time}."

    @property
    def pretty_start_time(self):
        return datetime.fromtimestamp(self.start_time).ctime()

    @property
    def runtime_timedelta(self):
        """
        :return: The runtime of the software as a `timedelta` object.
        """
        self._runtime_timedelta = str(timedelta(seconds=self.runtime_seconds))
        return self._runtime_timedelta

    @property
    def runtime_string(self):
        """
        :return: The runtime string representation of the program's runtime.
        """
        self._runtime_string = f"Program runtime was {self.runtime} {self._runtime_string_suffix}."
        return self._runtime_string

    # TODO: have this return a dict of 'number', 'resolution' instead of using string suffix?
    @property
    def runtime(self):
        """
        Return the runtime of the object.

        The method calculates and returns the runtime based on the value of the `runtime_seconds` property.
        If the `use_timedelta` property is set to `True`, the runtime is returned as a `timedelta` object.
        Otherwise, the runtime is returned as a numeric value representing either seconds, minutes, or hours,
        depending on the value of `runtime_seconds`.

        :return: The runtime of the object
        """
        if self._use_timedelta:
            self._runtime = self.runtime_timedelta
            self._runtime_string_suffix = 'HH:MM:SS'
        elif 60 < self.runtime_seconds < 3600:
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
        """
        :return: The runtime in seconds of the code block that was executed.
        """
        end_time = time.time()
        self._runtime_seconds =  round((end_time - self.start_time), 3)
        return self._runtime_seconds

    @property
    def runtime_minutes(self):
        """
        Compute the runtime of a process in minutes.

        :return: The runtime of the process in minutes.
        """
        self._runtime_minutes = (self.runtime_seconds / 60)
        if self._runtime_minutes <= 1:
            self._runtime_minutes = round(self._runtime_minutes, 3)
        else:
            self._runtime_minutes = round(self._runtime_minutes, 2)
        return self._runtime_minutes

    @property
    def runtime_hours(self):
        """
        Calculate and return the runtime in hours.

        :return: The runtime of the object in hours.
        """
        self._runtime_hours = (self.runtime_seconds / 60 / 60)
        if self._runtime_hours <= 1:
            self._runtime_hours = round(self._runtime_hours, 3)
        else:
            self._runtime_hours = round(self._runtime_hours, 2)
        return self._runtime_hours

    def write_runtime(self, **kwargs):
        save_file_path = Path(kwargs.get('save_file_path', '../Misc_Project_Files/last_runtime.txt'))
        as_text = kwargs.get('as_text', False)
        as_json = kwargs.get('as_json', False)

        if as_text and as_json:
            raise ValueError("both as_text and as_json cannot be True.")
        elif as_text:
            with open(save_file_path, 'w') as f:
                f.write(str(self))
                f.write('\n')
                f.write(self.runtime_string)
            print(f"runtime output to {save_file_path}")
        elif as_json:
            if save_file_path.suffix != '.json':
                save_file_path = save_file_path.with_suffix('.json')
            with open(save_file_path, 'w') as f:
                import json
                json.dump({'program_start_time': self.pretty_start_time,
                           'program_runtime': self.runtime},
                          f, indent=4)
            print(f"runtime output to {save_file_path.resolve()}")
        else:
            raise ValueError("Invalid output format. as_text or as_json must be True.")
