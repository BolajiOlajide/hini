# Standard library imports
import os
import json
from logging import getLogger

# Related third party imports.
from flask import (
    Flask, request, make_response,
    url_for, render_template
)
from slackclient import SlackClient
from dotenv import load_dotenv
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dateparser import parse
from timber import TimberHandler

# Local application imports.
from config import config
from utils.form_elements import elements, link_button_element
from model import db, User, Team
from utils.get_auth import get_authorization_credentials
from credentials import google_credentials
from utils.custom_ops import send_message, get_users_email, get_or_create_user, get_bot_token
from utils.get_credentials import credentials_to_dict, credentials_from_user
from utils.event_format import event_format
from utils.custom_date import add_minutes, normalize_date


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Timber API KEY
TIMBER_API_KEY = os.getenv('TIMBER_API_KEY')
# Your app's Slack bot user token
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
SLACK_CLIENT_ID = os.getenv('SLACK_CLIENT_ID')
SLACK_CLIENT_SECRET = os.getenv('SLACK_CLIENT_SECRET')
FLASK_ENV = os.getenv('FLASK_ENV') or 'development'

logger = getLogger("hini")
import pdb; pdb.set_trace()
timberhandler = TimberHandler(apikey=TIMBER_API_KEY)
logger.addHandler(timberhandler)
logger('starting application')

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


@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def index():
    return render_template('index.html')


@app.route('/mohini', methods=['GET', 'POST', 'OPTIONS'])
def mohini():
    return make_response('Mohini', 200)


@app.route("/invite", methods=["POST"])
def message_actions():
    try:
        _team_id = request.form.get('team_id', None)
        if not _team_id:
            _payload = json.loads(request.form.get('payload'))
            _team_id = _payload.get('team').get('id')
        bot_token = get_bot_token(_team_id, Team)

        # Slack client for Web API requests
        slack_client = SlackClient(bot_token)

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

        user_object = {
            'slack_username': slack_username,
            'slack_uid': slack_uid,
            'email': email,
            'tz': tz,
            'first_name': first_name,
            'last_name': last_name,
            'team_id': team_id
        }

        user = get_or_create_user(User, user_object)

        if not user.google_token:
            authorization_url, state = get_authorization_credentials(
                                        google_credentials, email)
            link_button_element[0]['actions'][0]['url'] = authorization_url
            send_message(
                "First time user, please authorize Hini with your google account",
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
            team_id = payload.get('team').get('id')
            ok, is_channel, emails = get_users_email(channel_id, slack_client, User, team_id)
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

            timezone = user.tz or '+0100'

            event_name = payload.get('submission').get('event_name')
            event_description = payload.get('submission').get('event_description')
            start_time = parse(
                payload.get('submission').get('start_time'),
                settings={
                    'TIMEZONE': timezone,
                    'RETURN_AS_TIMEZONE_AWARE': True
                }
            )
            duration = payload.get('submission').get('duration')
            end_time = add_minutes(start_time, duration)

            event_body = event_format(
                event_name,
                event_description,
                tz,
                normalize_date(start_time),
                normalize_date(end_time),
                emails
            )
            event = calendar.events().insert(
                calendarId='primary', body=event_body
            ).execute()
            send_message(
                'EVENT CREATED: {}'
                .format(event.get('htmlLink')),
                slack_client,
                slack_uid,
            )
        return make_response("", 200)
    except:  # noqa: #722
        return make_response('Error while processing your request!', 200)


@app.route('/authorize')
def authorize():
    try:
        code = request.args.get('code')
        scope = request.args.get('scope')
        state = request.args.get('state')

        if not (scope and code and state):
            return render_template('error.html')

        user = User.query.filter_by(state=state).first()

        if not user:
            return render_template('error.html')

        team_id = user.team_id
        bot_token = get_bot_token(team_id, Team)

        # Slack client for Web API requests
        slack_client = SlackClient(bot_token)

        flow = Flow.from_client_config(
                google_credentials, scopes=scope, state=state)

        flow.redirect_uri = url_for(
            'authorize', _external=True)

        # Use the authorization server's response to
        # fetch the OAuth 2.0 tokens.
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
        return render_template('success.html')
    except:  # noqa: #722
        return render_template('error.html')


@app.route('/addslack')
def add_slack():
    try:
        code = request.args.get('code')
        state = request.args.get('state')

        # An empty string is a valid token for this request
        temp_sc = SlackClient("")

        # Request the auth tokens from Slack
        auth_response = temp_sc.api_call(
            "oauth.access",
            client_id=SLACK_CLIENT_ID,
            client_secret=SLACK_CLIENT_SECRET,
            code=code
        )

        user_token = auth_response['access_token']
        bot_token = auth_response['bot']['bot_access_token']
        team_id = auth_response['team_id']
        team_name = auth_response['team_name']
        team = Team(
            code=code,
            bot_token=bot_token,
            user_token=user_token,
            team_name=team_name,
            team_id=team_id
        )
        team.save()
        return render_template('add_successful.html')
    except:  # noqa: #722
        return render_template('error.html')


if __name__ == "__main__":
    try:
        manager.run()
    except SystemError:
        print('Check the system. Something is wrong 😢')
