"""
HOBO-link:
HTTP requests and OATH authentication functions

See LICENSE and AUTHORS for more info
"""

import logging
from . import hobo_config_import as config

from datetime import datetime, timedelta
from requests.exceptions import HTTPError
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient, TokenExpiredError
from .hobo_time_util import datetime_to_datestr

#
# Get Oauth handle
#
def get_oauth():
    """Starts Oauth session."""
    cfg = config.get_config()
    if "oauth" in cfg:
        return cfg["oauth"]

    # First call - initiate oauth session
    if "client" not in cfg:
        client_id = cfg["client_id"]
        client = BackendApplicationClient(client_id=client_id)
        cfg["client"] = client
    else:
        client = cfg["client"]

    oauth = OAuth2Session(client=client)
    cfg["oauth"] = oauth
    return oauth


#
# Fetch (or refresh) token for HOBO connect
#
def fetch_token(refresh=False):
    """Fetch or refresh Oauth token."""
    cfg = config.get_config()
    if "token" in cfg and not refresh:
        # Just return the saved token
        return cfg["token"]

    # Get token from Oauth session
    token_endpoint = cfg["token_endpoint"]
    client_id = cfg["client_id"]
    client_secret = cfg["client_secret"]

    oauth = get_oauth()

    if not refresh:
        # Get a new token
        token = oauth.fetch_token(
            token_url=token_endpoint, client_id=client_id, client_secret=client_secret
        )

    else:
        # Refresh token
        # TODO: fix fetch_token(refresh=True)
        # Not documented by Onset...
        # token = oauth.refresh_token(token_url=token_endpoint,
        token = oauth.fetch_token(
            token_url=token_endpoint, client_id=client_id, client_secret=client_secret
        )

    # Save token
    cfg["token"] = token
    return token


#
# HOBOLink: Request for sensor data
#
# API error codes:
# https://webservice.hobolink.com/ws/data/info/index.html
#
def api_query(logger, start_date_time=None, end_date_time=None):
    """Makes an API request for data on individual loggers."""
    if start_date_time is None:
        raise ValueError("start_date_time not set")
    if not isinstance(start_date_time, datetime):
        raise TypeError("expected start_date_time to be a datetime object")

    cfg = config.get_config()

    min_api_time_delta = cfg["min_api_time_delta_minutes"]

    start_date_time_str = datetime_to_datestr(start_date_time)
    if end_date_time is None:
        raise ValueError("end_date_time not set")
    if not isinstance(end_date_time, datetime):
        raise TypeError("expected end_date_time to be a datetime object")
    if end_date_time <= start_date_time:
        # hobo api seems to hang if the end date less or equal to the
        # start date.  Raise an exception here to avoid that
        raise ValueError("end_date_time >= start_date_time")
    if end_date_time - start_date_time < timedelta(minutes=min_api_time_delta):
        # make sure we are getting at least min_api_time_delta minutes of data
        end_date_time = start_date_time + timedelta(minutes=min_api_time_delta)

    end_date_param_str = datetime_to_datestr(end_date_time)

    #
    # Construct request to submit
    #
    req = f"{cfg['query_endpoint']}/{cfg['user_id']}?"
    req += f"loggers={logger}&"
    req += f"start_date_time={start_date_time_str}&"
    req += f"end_date_time={end_date_param_str}"
    logging.debug(f"[HOBO-log] Sending request to HOBOLink: [{req}]")

    oauth = get_oauth()

    if "token" not in cfg:
        fetch_token()

    cfg = config.get_config()
    req_timeout = cfg["request_timeout"]

    try:
        r = oauth.get(req, timeout=req_timeout)
        r.raise_for_status()
        r_json = r.json()
        r_msg = r_json["message"]
        logging.debug(f"[HOBO-log] Query {r_msg}")
        return r_json
    except TokenExpiredError:
        fetch_token(refresh=True)
        r = oauth.get(req, timeout=req_timeout)
        r.raise_for_status()
        r_json = r.json()
        return r_json
    except HTTPError as http_error_msg:
        logging.error(f"[HOBO-log] Request error: {http_error_msg}")
        return None
