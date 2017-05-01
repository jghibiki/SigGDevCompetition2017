import datetime
import math

import config

class Enterprise:

    def __init__(self):

        self.failed = False

        self.funds = config.starting_funds
        self.monthly_quota = config.monthly_quota

        self.current_day = 1
        self.current_month = 1

        self.month_time_delta = datetime.timedelta(minutes=config.month_time_length[0], seconds=config.month_time_length[1])
        self.end_of_month = datetime.datetime.now() + self.month_time_delta

    def is_end_of_month(self):
        now = datetime.datetime.now()
        return now > self.end_of_month



    def update(self):

        if not self.is_end_of_month():

            now = datetime.datetime.now()
            diff = self.end_of_month - now

            percentage = 1.0 - ( diff.total_seconds() / self.month_time_delta.total_seconds())

            self.current_day = math.ceil(percentage * 32)

        else:
            self.failed = True





