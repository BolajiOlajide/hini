def send_message(text, slack_client, channel, attachment=None):
    return slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        as_user=True,
        text=text,
        attachments=attachment
    )


def get_bot_token(team_id, TeamModel):
    team_info = TeamModel.query.filter_by(
            team_id=team_id
        ).first()
    bot_token = team_info.bot_token
    return bot_token


def get_channel_info(channel_id, slack_client):
    return slack_client.api_call(
        "channels.info",
        channel=channel_id,
    )


def get_user_info(user_id, slack_client):
    try:
        # Get current user's information
        user_response = slack_client.api_call(
            "users.info",
            user=user_id
        )
        if not user_response.get('ok'):
            return None
        return user_response.get('user')
    except:  # noqa: #722
        return None


def get_or_create_user(User, user_object, slack_client=None):
    slack_uid = user_object.get('slack_uid')
    team_id = user_object.get('team_id')
    user = User.query.filter_by(
        slack_uid=slack_uid,
        team_id=team_id
    ).first()

    if (not user) and slack_client:
        user_info = get_user_info(slack_uid, slack_client)

        if user_info.get('is_bot'):
            return False

        slack_username = user_info.get('profile').get('display_name', '')
        tz = user_info.get('tz', '')
        email = user_info.get('profile').get('email', '')
        first_name = user_info.get('profile').get('first_name', '')
        last_name = user_info.get('profile').get('last_name', '')
        slack_uid = user_info.get('id')
        team_id = user_info.get('profile').get('team')

        user_object = {
            'slack_username': slack_username,
            'slack_uid': slack_uid,
            'email': email,
            'tz': tz,
            'first_name': first_name,
            'last_name': last_name,
            'team_id': team_id
        }

    if not user:
        user = User(
            slack_username=user_object.get('slack_username'),
            slack_uid=user_object.get('slack_uid'),
            email=user_object.get('email'),
            tz=user_object.get('tz'),
            first_name=user_object.get('first_name'),
            last_name=user_object.get('last_name'),
            team_id=user_object.get('team_id')
        )
        user.save()

    return user


def get_user_email(User, user_id, team_id, slack_client):
    user_object = {
        'slack_uid': user_id,
        'team_id': team_id
    }
    user_info = get_or_create_user(User, user_object, slack_client)
    email = user_info.email if user_info else {}
    return {'email': email}


def clean_email_list(email_list):
    return [email for email in email_list if email.get('email')]


def get_users_email(channel_id, slack_client, User, team_id):
    channel_info = get_channel_info(channel_id, slack_client)
    ok = channel_info.get('ok')
    is_channel = channel_info.get('channel').get('is_channel')
    members = channel_info.get('channel').get('members', [])
    members_email = [
        get_user_email(User, user_id, team_id, slack_client) for user_id in members
    ]
    return ok, is_channel, clean_email_list(members_email)
