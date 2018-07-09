import datetime
import pytz


def add_days(number_of_days):
    current_date = datetime.datetime.now(tz=pytz.utc)
    return current_date + datetime.timedelta(days=number_of_days)
