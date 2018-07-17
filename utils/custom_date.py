import datetime
# import pytz


def add_minutes(start_date, number_of_minutes):
    # current_date = datetime.datetime.now(tz=pytz.utc)
    return start_date + datetime.timedelta(minutes=int(number_of_minutes))
