import datetime
# import pytz


def add_minutes(start_date, number_of_minutes):
    # current_date = datetime.datetime.now(tz=pytz.utc)
    return start_date + datetime.timedelta(minutes=int(number_of_minutes))


def normalize_date(date_string):
    split_date = str(date_string).split(' ')
    return 'T'.join(split_date)
