import argparse

try:
    from oauth2client import client
    from oauth2client import tools
except ImportError:
    raise ImportError(
        'googleapiclient.sample_tools requires oauth2client. ' +
        'Please install oauth2client and try again.'
    )

from credentials import google_credentials


def create_access_token():
    scope = 'https://www.googleapis.com/auth/calendar'

    # Parser command-line arguments.
    parent_parsers = [tools.argparser]
    parent_parsers.extend([])
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=parent_parsers)
    flags = parser.parse_args('Hini')

    # Set up a Flow object to be used if we need to authenticate.
    message = tools.message_if_missing(google_credentials)
    flow = client.flow_from_clientsecrets(google_credentials,
                                          scope=scope,
                                          message=message)

    credentials = tools.run_flow(flow, storage, flags)

    return credentials
