# ELements for Slack dialog
elements = [
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
        "label": "Start Time",
        "type": "text",
        "name": "start_time",
        "placeholder": "Example: 10PM 12th of July 2018"
    },
    {
        "label": "Duration",
        "type": "select",
        "name": "duration",
        "options": [
            {
                "label": "15 minutes",
                "value": 15
            },
            {
                "label": "30 minutes",
                "value": 30
            },
            {
                "label": "1 hour",
                "value": 60
            },
            {
                "label": "1 hour 30 minutes",
                "value": 90
            },
            {
                "label": "2 hours",
                "value": 120
            },
            {
                "label": "2 hours 30 minutes",
                "value": 150
            },
            {
                "label": "3 hours",
                "value": 180
            }
        ]
    }
]

link_button_element = [
    {
        "fallback":
            "Upgrade your Slack client to use messages like these.",
        "color": "#E8E8E8",
        "actions": [
            {
                "type": "button",
                "text": "Authorize Hini"
            }
        ]
    }
]
