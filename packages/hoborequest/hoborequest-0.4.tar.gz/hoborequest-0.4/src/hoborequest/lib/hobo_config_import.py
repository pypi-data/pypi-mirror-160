"""
HOBO-config-import:
Imports configuration for HOBO-connect and HSDS

See LICENSE and AUTHORS for more info
"""

import os
import logging
import configparser

cfg = {}


def _import_config():
    """Import config for HOBOLink and HSDS"""

    conf_filename = "hobo-connect.conf"
    search_dirs = ("/conf", "./conf", ".", "../conf", "../../conf")
    conf_path = None
    for search_dir in search_dirs:
        path = os.path.join(search_dir, conf_filename)
        if os.path.exists(path):
            conf_path = path
            break
    if conf_path is None:
        logging.error(f"[HOBO-conf] Unable to find config file: {conf_filename}")
        raise FileNotFoundError()
    try:
        config = configparser.ConfigParser()
        config.read_file(open(conf_path))
    except:
        print("")
        print("[HOBO-error]:")
        print('File "hobo-connect.conf" not found.')
        print('Please edit "conf/hobo-connect.conf-SAMPLE" and rename it.')
        print("")
        raise

    #
    # HOBOLink: Query endpoint + constants
    #
    cfg["query_endpoint"] = config["HOBO"]["query_endpoint"]
    cfg["user_id"] = config["HOBO"]["user_id"]

    #
    # HOBOLink: Token endpoint + credentials
    #
    cfg["token_endpoint"] = config["HOBO"]["token_endpoint"]
    # pull client_id and client_secret from env variable to avoid
    # having to put these in a file
    if "HOBO_CLIENT_ID" in os.environ:
        logging.debug("reading client id from env")
        cfg["client_id"] = os.environ["HOBO_CLIENT_ID"]
    else:
        cfg["client_id"] = config["HOBO"]["client_id"]
    if "HOBO_CLIENT_SECRET" in os.environ:
        logging.debug("reading client secret from env")
        cfg["client_secret"] = os.environ["HOBO_CLIENT_SECRET"]
    else:
        cfg["client_secret"] = config["HOBO"]["client_secret"]

    #
    # HOBOLink: API query parameters:
    # start/end time, polling interval, request timeout
    #
    if config["HOBO"]["start_date_time"]:
        # For precise time-slicing:
        cfg["start_date_time"] = config["HOBO"]["start_date_time"]
        cfg["end_date_time"] = config["HOBO"]["end_date_time"]
        logging.info(f'[HOBO-connect] Start: {cfg["start_date_time"]} UTC')
        logging.info(
            f'[HOBO-connect] Time slice: {cfg["start_date_time"]} --> {cfg["end_date_time"]}'
        )
    else:
        # For requesting the most recent data:
        # Compute start and end times with each request
        cfg["start_date_time"] = None
        cfg["end_date_time"] = None

    if config["HOBO"]["polling_interval_minutes"]:
        polling_interval = int(config["HOBO"]["polling_interval_minutes"])
        cfg["polling_interval"] = polling_interval
        logging.info(
            f"[HOBO-connect] Using polling interval: {polling_interval} minute(s)"
        )
    else:
        polling_interval = None
        logging.info("polling interval is None")
        cfg["polling_interval"] = polling_interval

    cfg["request_timeout"] = float(config["HOBO"]["request_timeout"])
    cfg["max_map_items"] = int(config["HOBO"]["max_map_items"])
    cfg["max_api_query_items"] = int(config["HOBO"]["max_api_query_items"])
    cfg["min_api_time_delta_minutes"] = int(
        config["HOBO"]["min_api_time_delta_minutes"]
    )
    if cfg["min_api_time_delta_minutes"] <= 0:
        logging.error("min_api_time_delta_minutes config not valid")
        raise ValueError()
    cfg["max_api_time_delta_minutes"] = int(
        config["HOBO"]["max_api_time_delta_minutes"]
    )
    if cfg["max_api_time_delta_minutes"] <= 0:
        logging.error("max_api_time_delta config not valid")
        raise ValueError()

    cfg["hsds_filename"] = config["HSDS"]["hsds_filename"]
    cfg["hsds_endpoint"] = config["HSDS"]["hsds_endpoint"]

    #
    # Metadata config
    #
    cfg["meta_repo"] = config["META"]["meta_repo"]
    cfg["meta_local_dir"] = config["META"]["meta_local_dir"]
    cfg["meta_root_path"] = config["META"]["meta_root_path"]
    cfg["meta_loggers_dir"] = config["META"]["meta_loggers_dir"]
    cfg["meta_sensors_dir"] = config["META"]["meta_sensors_dir"]


def get_config():
    """Return config map."""
    if len(cfg) == 0:
        _import_config()
    return cfg
