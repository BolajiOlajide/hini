def send_message(text, slack_client, channel, attachment=None):
    return slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        as_user=True,
        text=text,
        attachments=attachment
    )
