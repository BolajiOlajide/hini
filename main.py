import os
import json

from flask import Flask, request, make_response, jsonify, redirect
from slackclient import SlackClient
from dotenv import load_dotenv
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from google_auth_oauthlib.flow import InstalledAppFlow

from config import config
from utils.form_elements import elements, link_button_element
from user import db, User
from utils.get_auth import get_authorization_credentials
from credentials import google_credentials
from utils.message import send_message


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
        return make_response('', 200)

    # if ('payload' not in request.form.keys()):
    #     trigger_id = request.form['trigger_id']
    #     print(request.form)
    #     print("")
    #     slack_client.api_call(
    #         "dialog.open",
    #         trigger_id=trigger_id,
    #         dialog={
    #             "title": "Create an event",
    #             "submit_label": "Create",
    #             "callback_id": user_id + "calender_invite",
    #             "notify_on_cancel": True,
    #             "elements": elements
    #         }
    #     )
    # else:
    #     print(request.form)
    #     payload = json.loads(request.form['payload'])
    #     submission = payload['submission']
    #     print(submission)
    return make_response('Working...', 200)


@app.route('/authorize')
def authorize():
    code = request.args.get('code')
    scope = request.args.get('scope')
    state = request.args.get('state')
    if not (scope and code and state):
        return make_response('Invalid Parameters', 400)
    return make_response('Smooth!', 400)


if __name__ == "__main__":
    try:
        manager.run()
    except SystemError:
        print('Check the system. Something is wrong 🚀')
