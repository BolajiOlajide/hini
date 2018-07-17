import os
import json

from flask import (
    Flask, request, make_response,
    jsonify, url_for
)
from slackclient import SlackClient
from dotenv import load_dotenv
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dateparser import parse

from config import config
from utils.form_elements import elements, link_button_element
from model import db, User
from utils.get_auth import get_authorization_credentials
from credentials import google_credentials
from utils.custom_ops import send_message, get_users_email
from utils.get_credentials import credentials_to_dict, credentials_from_user
from utils.dict_formatter import dict_to_binary
from utils.event_format import event_format
from utils.custom_date import add_minutes


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Your app's Slack bot user token
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
SLACK_VERIFICATION_TOKEN = os.getenv('SLACK_VERIFICATION_TOKEN')
FLASK_ENV = os.getenv('FLASK_ENV') or 'development'
QUOTE_BASE_URL = os.getenv('QUOTE_BASE_URL')

# Slack client for Web API requests
slack_client = SlackClient(SLACK_BOT_TOKEN)

# Flask web server for incoming traffic from Slack
app = Flask(__name__)

# Define configuration settings for Hini app
app.config.from_object(config[FLASK_ENV])

# Instantiate the Manager from Flask Script
db.init_app(app)
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server())

# Send a message to the user asking if they would like coffee
user_id = "hinii"


@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def index():
    return jsonify({
        'status': 'success',
        'message': 'Mohini\'s the greatest'
    }), 200


@app.route("/invite", methods=["POST"])
def message_actions():
    user_id = request.form.get('user_id')

    if not user_id:
        payload = json.loads(request.form['payload'])
        user_id = payload.get('user').get('id')

    # Get current user's information
    user_response = slack_client.api_call(
        "users.info",
        user=user_id
    )

    if not user_response.get('ok'):
        return make_response('Error getting user profile.', 400)

    user_info = user_response.get('user')

    slack_username = user_info.get('profile').get('display_name', '')
    tz = user_info.get('tz', '')
    email = user_info.get('profile').get('email', '')
    first_name = user_info.get('profile').get('first_name', '')
    last_name = user_info.get('profile').get('last_name', '')
    slack_uid = user_info.get('id')
    team_id = user_info.get('profile').get('team')

    user = User.query.filter_by(
        slack_uid=slack_uid,
        team_id=team_id
    ).first()

    if not user:
        user = User(
            slack_username=slack_username,
            slack_uid=slack_uid,
            email=email,
            tz=tz,
            first_name=first_name,
            last_name=last_name,
            team_id=team_id
        )
        user.save()

    if not user.google_token:
        authorization_url, state = get_authorization_credentials(
                                    google_credentials, email)
        link_button_element[0]['actions'][0]['url'] = authorization_url
        send_message(
            "First time user, please connect Hini to your Google Calendar",
            slack_client,
            slack_uid,
            link_button_element
        )
        user.state = state
        user.save()
        return make_response('', 200)

    if ('payload' not in request.form.keys()):
        trigger_id = request.form['trigger_id']
        slack_client.api_call(
            "dialog.open",
            trigger_id=trigger_id,
            dialog={
                "title": "Create an event",
                "submit_label": "Create",
                "callback_id": user_id + "calender_invite",
                "notify_on_cancel": True,
                "elements": elements
            }
        )
    else:
        payload = json.loads(request.form['payload'])
        channel_id = payload.get('channel').get('id')
        ok, is_channel, emails = get_users_email(channel_id, slack_client)
        if not ok:
            send_message(
                'Error retrieving channel info!',
                slack_client,
                slack_uid,
            )
        if not is_channel:
            send_message(
                'Can only use Hini in a channel for now.',
                slack_client,
                slack_uid,
            )
        if not payload.get('submission'):
            return make_response('', 200)
        credentials = Credentials(**credentials_from_user(user))

        calendar = build('calendar', 'v3', credentials=credentials)

        event_name = payload.get('submission').get('event_name')
        event_description = payload.get('submission').get('event_description')
        start_time = parse(payload.get('submission').get('start_time'))
        duration = payload.get('submission').get('duration')
        end_time = add_minutes(start_time, duration)
        print(emails)
        event_body = event_format(
            event_name,
            event_description,
            tz,
            start_time,
            end_time,
            emails
        )
        event = calendar.events().insert(calendarId='primary', body=event_body).execute()
        print('Event created: %s' % (event.get('htmlLink')))
        return make_response('EVENT CREATED: {}'.format(event.get('htmlLink')), 200)
    return make_response('Working...', 200)


@app.route('/authorize')
def authorize():
    try:
        code = request.args.get('code')
        scope = request.args.get('scope')
        state = request.args.get('state')

        if not (scope and code and state):
            return make_response('Invalid Parameters', 400)

        user = User.query.filter_by(state=state).first()

        if not user:
            return make_response('Invalid parameters', 400)

        flow = Flow.from_client_config(
                google_credentials, scopes=scope, state=state)

        flow.redirect_uri = url_for(
            'authorize', _external=True)

        # Use the authorization server's response to fetch the OAuth 2.0 tokens.
        authorization_response = request.url
        flow.fetch_token(authorization_response=authorization_response)

        credentials = credentials_to_dict(flow.credentials)

        user.google_token = credentials.get('token')
        user.refresh_token = credentials.get('refresh_token')
        user.save()
        send_message(
            f"Google calender for email - {user.email} successfully authorized.",
            slack_client,
            user.slack_uid
        )
        return make_response('User successfully authenticated!', 400)
    except:
        return make_response('Error', 400)


if __name__ == "__main__":
    try:
        manager.run()
    except SystemError:
        print('Check the system. Something is wrong 😢')
