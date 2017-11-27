"""
This module contains functionalities related with date-time util 
"""
import time, calendar


class DateTimeUtils:
    # Current time-stamp integer.
    @staticmethod
    def time_to_int():
        return int(calendar.timegm(time.gmtime()))

# if __name__ == "__main__":
#     print DateTimeUtils.time_to_int()