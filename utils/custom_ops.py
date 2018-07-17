def send_message(text, slack_client, channel, attachment=None):
    return slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        as_user=True,
        text=text,
        attachments=attachment
    )


def get_channel_info(channel_id, slack_client):
    return slack_client.api_call(
        "channels.info",
        channel=channel_id,
    )


def get_user_email(user_id, slack_client):
    user_info = slack_client.api_call(
        "users.info",
        user=user_id,
    ).get('user')
    email = user_info.get('profile').get('email')
    return {'email': email}


def clean_email_list(email_list):
    return [email for email in email_list if email.get('email')]


def get_users_email(channel_id, slack_client):
    channel_info = get_channel_info(channel_id, slack_client)
    ok = channel_info.get('ok')
    is_channel = channel_info.get('channel').get('is_channel')
    members = channel_info.get('channel').get('members', [])
    members_email = [
        get_user_email(user_id, slack_client) for user_id in members
    ]
    return ok, is_channel, clean_email_list(members_email)
