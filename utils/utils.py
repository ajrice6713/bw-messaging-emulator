from datetime import datetime

def datetime_to_float(d):
    epoch = datetime.fromtimestamp(0)
    total_seconds =  (d - epoch).total_seconds()
    return total_seconds


def float_to_datetime(fl):
    return datetime.fromtimestamp(fl)
