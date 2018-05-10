import os
from random import randint

from flask import Flask, request, make_response
from slackclient import SlackClient
from dotenv import load_dotenv
from flask_script import Manager, Server
from quotes import quotes

from config import config


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
manager = Manager(app)
manager.add_command('runserver', Server())

# Dictionary to store coffee orders. In the real world, you'd want an actual
# key-value store
COFFEE_ORDERS = {}

# Send a message to the user asking if they would like coffee
user_id = "hinii"

# order_dm = slack_client.api_call(
#   "chat.postMessage",
#   as_user=True,
#   channel=user_id,
#   text="I am Coffeebot ::robot_face::, and I\'m here to help bring you \
#     fresh coffee :coffee:",
#   attachments=[{
#     "text": "",
#     "callback_id": user_id + "coffee_order_form",
#     "color": "#3AA3E3",
#     "attachment_type": "default",
#     "actions": [{
#       "name": "coffee_order",
#       "text": ":coffee: Order Coffee",
#       "type": "button",
#       "value": "coffee_order"
#     }]
#   }]
# )

# Create a new order for this user in the COFFEE_ORDERS dictionary
# COFFEE_ORDERS[user_id] = {
#     "order_channel": order_dm["channel"],
#     "message_ts": "",
#     "order": {}
# }


@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def index():
    print('checking the index')
    return make_response('Mohini\'s the greatest', 200)


@app.route('/proton', methods=['POST', 'OPTIONS'])
def proton():
    word_length = len(quotes)
    random_index = randint(0, (word_length - 1))
    return make_response(quotes[random_index], 200)


@app.route("/invite_info", methods=["POST"])
def message_actions():
    trigger_id = request.form['trigger_id']
    print(request.form)
    print("")
    open_dialog = slack_client.api_call(
        "dialog.open",
        trigger_id=trigger_id,
        dialog={
            "title": "Create an event",
            "submit_label": "Create",
            "callback_id": user_id + "coffee_order_form",
            "notify_on_cancel": True,
            "elements": [
                {
                    "label": "Event Name",
                    "type": "text",
                    "name": "event_name",
                    "placeholder": "Enter the name of the event"
                },
                {
                    "label": "Event description",
                    "type": "textarea",
                    "name": "event_description",
                    "placeholder": "Enter the description of the event"
                },
                {
                    "label": "Reminder (email)",
                    "type": "select",
                    "name": "email_reminder",
                    "placeholder": "Set email reminder",
                    "options": [
                        {
                            "label": "No reminder",
                            "value": 0
                        },
                        {
                            "label": "5 minutes",
                            "value": 5
                        },
                        {
                            "label": "10 minutes",
                            "value": 10
                        },
                        {
                            "label": "15 minutes",
                            "value": 15
                        },
                        {
                            "label": "20 minutes",
                            "value": 20
                        },
                        {
                            "label": "25 minutes",
                            "value": 25
                        },
                        {
                            "label": "30 minutes",
                            "value": 30
                        }
                    ]
                },
                {
                    "label": "Reminder (popup)",
                    "type": "select",
                    "name": "popup_reminder",
                    "placeholder": "Set popup reminder",
                    "options": [
                        {
                            "label": "No reminder",
                            "value": 0
                        },
                        {
                            "label": "5 minutes",
                            "value": 5
                        },
                        {
                            "label": "10 minutes",
                            "value": 10
                        },
                        {
                            "label": "15 minutes",
                            "value": 15
                        },
                        {
                            "label": "20 minutes",
                            "value": 20
                        },
                        {
                            "label": "25 minutes",
                            "value": 25
                        },
                        {
                            "label": "30 minutes",
                            "value": 30
                        }
                    ]
                }
            ]
        }
    )

    return make_response('Requesting information for invite', 200)


@app.route('/create_invite', methods=['POST'])
def test_something():
    print(request.form)
    print('testing 1.... 2.... 3....')
    return make_response('Bolaji wuz ere', 200)


if __name__ == "__main__":
    manager.run()
