import time

DT_FORMAT = "%Y-%m-%d_%H:%M:%S"

def format_dt(millis):
    return time.strftime(DT_FORMAT,time.gmtime(millis/1000))

