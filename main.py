import os
import json

from flask import Flask, request, make_response, jsonify
from slackclient import SlackClient
from dotenv import load_dotenv
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from config import config
from form_elements import elements
from user import db


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
    if ('payload' not in request.form.keys()):
        trigger_id = request.form['trigger_id']
        print(request.form)
        print("")
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
        print(request.form)
        payload = json.loads(request.form['payload'])
        submission = payload['submission']
        print(submission)
    return make_response('', 200)


if __name__ == "__main__":
    try:
        manager.run()
    except SystemError:
        print('Check the system. Something is wrong 🚀')
