import datetime


def validate_time_format(date):
    try:
        return datetime.datetime.strptime(date, "%Y%m%d")
    except ValueError:
        raise Exception('Incorrect format of time.')
