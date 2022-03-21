from datetime import datetime


def datetime_to_float(d):
    return d.timestamp()


def float_to_datetime(fl):
    return datetime.fromtimestamp(fl)
