from datetime import datetime, timedelta
from math import ceil


class RecordDatetime():
    # iminutes means int-type minutes
    def __init__(self, start_time: datetime, tomato_minutes: int) -> None:
        self.start_time = start_time
        # expected duration
        self.tomato_minutes = tomato_minutes
        self.break_time_iminutes = ceil(tomato_minutes/6)
        self.expected_duration_iminutes = tomato_minutes + self.break_time_iminutes
        self.expected_finish_time = self.start_time + \
            timedelta(minutes=tomato_minutes+self.break_time_iminutes)

    def is_actual_duration_valid(self, finish_time: datetime):
        self.finish_time = finish_time
        self.actual_duration = finish_time-self.start_time
        self.actual_duration_iminutes = int(
            self.actual_duration.total_seconds()/60)
        self.is_datetime_valid = self.actual_duration_iminutes >= \
            self.tomato_minutes and self.actual_duration < timedelta(days=1)
        return self.is_datetime_valid

    def working_duration_proportion(self):
        if self.is_datetime_valid:
            if self.actual_duration_iminutes == self.tomato_minutes:
                return 1
            return self.tomato_minutes/self.actual_duration_iminutes
        return 0
