from EasyLoggerAJM import EasyLogger


class WDLogger(EasyLogger):
    def __init__(self, *args, **kwargs):
        self.show_warning_logs_in_console = True
        self._is_daily_log_spec = True
        super().__init__(is_daily_log_spec=self._is_daily_log_spec,
                         show_warning_logs_in_console=self.show_warning_logs_in_console,
                         *args, ** kwargs)

