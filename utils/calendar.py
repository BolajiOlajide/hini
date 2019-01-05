from .custom_ops import send_message


async def create_event(calendar, event_body, slack_client, slack_uid):
    event = calendar.events().insert(
        calendarId='primary', body=event_body
    ).execute()

    send_message(
        'EVENT CREATED: {}'
        .format(event.get('htmlLink')),
        slack_client,
        slack_uid,
    )

    return True
