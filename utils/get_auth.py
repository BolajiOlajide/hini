from google_auth_oauthlib.flow import Flow


def get_authorization_credentials(google_credentials, email=''):
    # Use the client_secret.json file to identify the application requesting
    # authorization. The client ID (from that file)
    # and access scopes are required.
    flow = Flow.from_client_config(
        google_credentials,
        scopes=['https://www.googleapis.com/auth/calendar'])

    # Indicate where the API server will redirect the user
    # after the user completes
    # the authorization flow. The redirect URI is required.
    flow.redirect_uri = 'http://proton-dev.com:5000/authorize'

    # Generate URL for request to Google's OAuth 2.0 server.
    # Use kwargs to set optional request parameters.
    return flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # res-prompting the user for permission. Recommended
        # for web server apps.
        access_type='offline',
        login_hint=email,
        prompt='consent',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true'
    )
