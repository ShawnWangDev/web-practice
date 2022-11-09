from datetime import datetime, timedelta
from math import ceil


class RecordDatetime():
    # iminutes means int-type minutes
    def __init__(self, start_time: datetime, finish_time: datetime, total_tomato_duration: int) -> None:
        start_time_sec_round_down = start_time.replace(second=0, microsecond=0)
        # a person cannot create a record at 0 second time(such as 17:05:00)
        # then start the tomato immediately at 17:05:00.
        # so delay one minute(+timedelta(minutes=1)).
        self.start_time = start_time_sec_round_down+timedelta(minutes=1)
        self.finish_time = finish_time.replace(second=0, microsecond=0)
        self.total_tomato_duration_iminutes = total_tomato_duration
        # actual duration
        self.actual_duration = self.finish_time-self.start_time
        self.actual_duration_iminutes = int(
            self.actual_duration.total_seconds()/60)
        # expected duration
        self.break_time_iminutes = ceil(self.total_tomato_duration_iminutes/6)
        self.expected_duration_iminutes = self.total_tomato_duration_iminutes + \
            self.break_time_iminutes
        self.expected_finish_time = self.start_time + \
            timedelta(minutes=self.total_tomato_duration_iminutes)

    def is_actual_duration_valid(self):
        return self.actual_duration_iminutes >= self.total_tomato_duration_iminutes\
            and self.actual_duration < timedelta(days=1)

    def working_duration_proportion(self):
        if not self.is_actual_duration_valid():
            return 0
        if self.actual_duration_iminutes == self.total_tomato_duration_iminutes:
            return 1
        return self.actual_duration_iminutes/self.expected_duration_iminutes
