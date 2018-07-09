import os
from os.path import join, dirname

from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


google_credentials = {
    "web": {
        "client_id": GOOGLE_CLIENT_ID,
        "project_id": "hini-1530850449245",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token",
        "auth_provider_x509_cert_url":
            "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uris": [
            "http://proton-dev.com:5000/authorize",
            "http://localhost:5000/authorize"
        ],
        "javascript_origins":
            [
                "http://localhost:5000",
                "http://proton-dev.com:5000"
            ]
    }
}
