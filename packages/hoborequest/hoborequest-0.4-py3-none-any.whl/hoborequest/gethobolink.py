#!/usr/bin/env python3

"""
Get-HOBO-link:
Obtains data from HOBOLink loggers for testing purposes

See LICENSE and AUTHORS for more info
"""

import sys
import logging


from datetime import datetime, timedelta

if __name__ == "__main__":
    from lib.hobo_time_util import get_datetime
    from lib import hobo_link
    from lib import hobo_config_import as config
else:
    from .lib.hobo_time_util import get_datetime
    from .lib import hobo_link
    from .lib import hobo_config_import as config


#
# HOBO-config: CLI help and usage
#
def usage():
    """Prints CLI usage instructions."""
    print("[get-hobo-link] get data from hobo link HOBO-connect")
    print(
        "Usage: get-hobo-link.py [-h] [--loglevel debug|info|warning|error] [-n max-lines] [--start-date-time YYYY-MM-DD HH:MM:SS] [--end-date-time YYYY-MM-DD HH:MM:SS] <logger>"
    )
    print("   <logger>: logger serial number")
    print("Options:")
    print("   --help: this message")
    print("   --loglevel debug|info|warning|error: change default log level")
    print("   --start-date-time: start time")
    print("   --end-date-time: end time")
    print("   -n: max lines to be output")
    sys.exit(1)


#
# Get values for logger and print responses
#
def get_logger_values(logger, start_date_time=None, end_date_time=None, max_lines=0):
    """Get values for logger and print out responses."""

    max_results = True  # start with True, will set to False when there's no more data
    count = 0
    logging.info(
        f"get_logger_values - {logger}, start_date_time={start_date_time}, end_date_time={end_date_time}, max_lines={max_lines}"
    )

    while max_results:
        rsp = hobo_link.api_query(
            logger, start_date_time=start_date_time, end_date_time=next_date_time
        )
        if not rsp:
            logging.error("No response returned from api_query")
            break

        if "observation_list" not in rsp:
            logging.info("get_logger_values - observation_list not returned")
            logging.debug(f"get_logger_values - api_query response: {rsp}")
            break

        observation_list = rsp["observation_list"]
        if len(observation_list) == 0:
            logging.info("get_logger_values - no rows found in observation_list")
            break
        logging.info(f"get_logger_values - got {len(observation_list)} rows")

        if "max_results" not in rsp:
            max_results = False

        last_timestamp = None

        for row in observation_list:
            logger_sn = row["logger_sn"]
            sensor_sn = row["sensor_sn"]
            data_type_id = row["data_type_id"]
            si_value = row["si_value"]
            sensor_measurement_type = row["sensor_measurement_type"]
            timestamp = row["timestamp"]
            last_timestamp = get_datetime(timestamp)
            if last_timestamp >= end_date_time:
                logging.debug(
                    f"timestamp: {timestamp} >= end_date_time, stop row iteration"
                )
                break
            print(
                f"{logger_sn}, {sensor_sn}, {data_type_id}, {si_value}, {sensor_measurement_type}, {timestamp}"
            )
            count += 1
            if max_lines > 0 and count >= max_lines:
                max_results = False
                break
        start_date_time = last_timestamp
        logging.debug(f"get_logger_values - start_date_time next: {start_date_time}")
        if end_date_time is not None and start_date_time >= end_date_time:
            max_results = False

    logging.info(f"get_logger_values - fetched {count} items ")
    return count


#
# Main
#
if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
    usage()

logger_sns = []
log_level = None
start_date_time = None
end_date_time = None
max_lines = 0

# process cmd link args

argn = 1
while argn < len(sys.argv):
    arg = sys.argv[argn]
    val = None
    val2 = None
    if len(sys.argv) > argn + 1:
        val = sys.argv[argn + 1]
    if len(sys.argv) > argn + 2:
        val2 = sys.argv[argn + 2]
    if arg[0] == "-":
        # process option
        if arg == "--loglevel":
            log_level = val.upper()
            argn += 1
        elif arg in ("-h", "--help"):
            usage()
        elif arg == "-n":
            max_lines = int(val)
            argn += 1
        elif arg in ("-s", "--start-date-time"):
            start_date_time = val
            argn += 1
            if val2 is not None and val2.find(":") > 0:
                argn += 1
                # looks like a time, add to start_date_time
                start_date_time += f" {val2}"
            else:
                start_date_time += " 00:00:00"
        elif arg in ("-e", "--end-date-time"):
            end_date_time = val
            argn += 1
            if val2 is not None and val2.find(":") > 0:
                argn += 1
                # looks like a time, add to start_date_time
                end_date_time += f" {val2}"
            else:
                end_date_time += " 00:00:00"
        else:
            # unknown option
            usage()
    else:
        logger_sns.append(arg)
    argn += 1

cfg = config.get_config()

if start_date_time is None:
    start_date_time = cfg["start_date_time"]

if end_date_time is None:
    end_date_time = cfg["end_date_time"]

if not start_date_time:
    print("no start_date_time set!")
    sys.exit(1)

if not logger_sns:
    print("no logger specified")
    sys.exit(1)

start_date_time = get_datetime(start_date_time)

if end_date_time is None:
    end_date_time = datetime.utcnow()
else:
    end_date_time = get_datetime(end_date_time)

#
# Setup log level
#
if log_level is None:
    if "log_level" in cfg:
        log_level = cfg["log_level"]
    else:
        log_level = "DEBUG"

if log_level == "DEBUG":
    level = logging.DEBUG
elif log_level == "INFO":
    level = logging.INFO
elif log_level in ("WARN", "WARNING"):
    level = logging.WARNING
elif log_level == "ERROR":
    level = logging.ERROR
else:
    print(f"[HOBO-log] Unexpected log_level settings: {log_level}")
    sys.exit(1)

max_api_time_delta = cfg["max_api_time_delta_minutes"]
if max_api_time_delta <= 0:
    logging.error("max_api_time_delta config not set")
    sys.exit(1)

logging.basicConfig(level=level)

if len(logger_sns) == 1:
    logging.info(f"logger: {logger_sns[0]}")
else:
    logging.info(f"loggers: {logger_sns}")

logging.info(f"start_date_time: {start_date_time}")
logging.info(f"end_date_time: {end_date_time}")
logging.info(f"max_lines: {max_lines}")

print(
    "logger_sn, sensor_sn, data_type_id, si_value, sensor_measurement_type, timestamp"
)
count = 0
next_date_time = start_date_time

while start_date_time < end_date_time:
    logging.info(f"start_date_time: {start_date_time}")

    next_date_time = start_date_time + timedelta(minutes=max_api_time_delta)
    if next_date_time > end_date_time:
        next_date_time = end_date_time
    logging.info(f"next_date_time: {next_date_time}")

    for logger_sn in logger_sns:
        num_items = get_logger_values(
            logger_sn,
            start_date_time=start_date_time,
            end_date_time=next_date_time,
            max_lines=max_lines,
        )
        if num_items >= cfg["max_api_query_items"]:
            # we hit the limit of results that will returned for this time interval
            logging.warn("max_api_query_items returned")
        if max_lines > 0:
            max_lines -= num_items
            if max_lines <= 0:
                logging.info("fetched all requested lines")
                break
        count += num_items
    # paginate by polling_time minutes
    start_date_time = next_date_time

logging.info(f"get-hobo-link done, got {count} items")
