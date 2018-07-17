

def event_format(
    event_name,
    event_description,
    tz,
    start_time,
    end_time,
    emails
):
    return {
        'summary': event_name,
        'description': event_description,
        'start': {
            'dateTime': start_time.__str__(),
            'timeZone': tz
        },
        'end': {
            'dateTime': end_time.__str__(),
            'timeZone': tz
        },
        'attendees': emails,
        'reminders': {'useDefault': True},
    }
