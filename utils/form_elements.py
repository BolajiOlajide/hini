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
        "label": "Finish Date",
        "type": "text",
        "name": "finish_date",
        "placeholder": "Please follow the format: DD-MM-YYYY"
    },
    {
        "label": "Done Date",
        "type": "text",
        "name": "fidoh_date",
        "placeholder": "Please follow the format: DD-MM-YYYY"
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
