#!/usr/bin/env python3

"""
HOBO-connect:
Integrates HOBOLink loggers with HSDS

See LICENSE and AUTHORS for more info
"""

import os
import sys
import time
import logging
import numpy as np
import yaml
import h5pyd
import h5py


from collections import OrderedDict
from datetime import datetime, timedelta, timezone

if __name__ == "__main__":
    from lib.hobo_link import api_query
    import lib.hobo_config_import as config
    from lib.hobo_time_util import get_datetime, datestr_to_timestamp
    from lib.hobo_metadata import update_general, update_logger, update_sensor
    from lib.hobo_dtype import dt_measurements
else:
    from .lib.hobo_link import api_query
    from .lib import hobo_config_import as config
    from .lib.hobo_time_util import get_datetime, datestr_to_timestamp
    from .lib.hobo_metadata import update_general, update_logger, update_sensor
    from .lib.hobo_dtype import dt_measurements


sensor_map = {}  # map of sensor_sn's to ordered dict of timestamps


def h5File(path, mode="r"):
    """Open an HSDS domain or HDF5 file based on the path.
    If path starts with "hdf5://", use HSDS, otherwise
    use h5py on a regular file path."""

    logging.debug(f"[HOBO-log] Opening h5File: '{path}', mode: '{mode}'")
    if path.startswith("hdf5://"):
        kwargs = {"use_cache": False}
        if "HSDS_USERNAME" in os.environ:
            kwargs["username"] = os.environ["HSDS_USERNAME"]
        if "HSDS_PASSWORD" in os.environ:
            kwargs["password"] = os.environ["HSDS_PASSWORD"]
        cfg = config.get_config()
        endpoint = cfg["hsds_endpoint"]
        kwargs["endpoint"] = endpoint

        f = h5pyd.File(path, mode=mode, **kwargs)
    else:
        f = h5py.File(path, mode=mode)
    return f


#
# Fetch measurement type enum from HDF store
#
def get_measurement_types():
    """Read and measurement types from HDF store"""
    cfg = config.get_config()

    if "measurement_types" in cfg:
        # already gottent this
        return cfg["measurement_types"]

    measurement_types = {}

    # Open HDF store
    hsds_filename = cfg["hsds_filename"]
    logging.debug(f"[HOBO-log] Opening {hsds_filename}")

    with h5File(hsds_filename, mode="r") as f:
        grp = f["measurement_types"]
        values = grp.attrs["values"]
        num_rows = values.shape[0]
        logging.info(f"[HOBO-log] fetched {num_rows} measurement_types")
        for i in range(num_rows):
            value = values[i]
            measurement_types[value] = i
            logging.debug(f"[HOBO-log] Mapping measurement_type: {value} to {i}")

    # Save so we don't need to fetch each time
    cfg["measurement_types"] = measurement_types
    return measurement_types


#
# Get loggers
# Retrieve entire loggers dataset as an array
# Note: since the number of loggers is fairly small,
#       it's easiest just to grab then all here
#
def get_loggers():
    """Returns a list of loggers."""
    # Open HDF store
    cfg = config.get_config()
    hsds_filename = cfg["hsds_filename"]
    logging.debug(f"[HOBO-log] Opening {hsds_filename}")

    try:
        with h5File(hsds_filename, mode="r") as f:
            dset = f["loggers"]
            loggers = dset[...]  # read entire dataset
    except Exception as e:
        logging.error(f"[HOBO-log] {e}")
        sys.exit("[HOBO-log] Fatal error: exiting")

    return loggers


#
# Update the given row of the logger with last query time
#
def update_logger_last_query(logger_index, last_query):
    """Updates the field last_query in the logger."""
    cfg = config.get_config()
    hsds_filename = cfg["hsds_filename"]
    logging.debug(f"[HOBO-log] Opening {hsds_filename}")

    last_query_ts = last_query.replace(tzinfo=timezone.utc).timestamp()

    with h5File(hsds_filename, mode="a") as f:
        dset = f["loggers"]
        logger = dset[logger_index]
        current_ts = logger["last_query"]
        if last_query_ts < current_ts:
            msg = f"skip updating last_query for logger: {logger_index} - "
            msg += f"last_query_ts: {last_query_ts} is less than "
            msg += f"current value: {current_ts}"
            logging.warning(msg)
        else:
            logger["last_query"] = last_query_ts
            dset[logger_index] = logger  # update row


#
# Get the last_query time as a datetime object
#
def get_logger_last_query(logger_index):
    """Returns the timestamp of the logger last query."""
    cfg = config.get_config()
    hsds_filename = cfg["hsds_filename"]
    last_query_ts = None
    logging.debug(f"[HOBO-log] Opening {hsds_filename}")
    with h5File(hsds_filename, mode="r") as f:
        dset = f["loggers"]
        logger = dset[logger_index]
        last_query_ts = logger["last_query"]
    if not last_query_ts:
        logging.warning(f"[HOBO-log] last_query not set for logger {logger_index}")
        last_query = None
    else:
        last_query = datetime.utcfromtimestamp(last_query_ts)
    return last_query


def hsds_last_update_time():
    """Return last update timestamp"""
    cfg = config.get_config()
    hsds_filename = cfg["hsds_filename"]
    last_update_ts = 0

    with h5File(hsds_filename, mode="r") as f:
        if "last_updated_data" in f.attrs:
            last_update_ts = f.attrs["last_updated_data"]
    return last_update_ts


def is_duplicate(row):
    """Verifies and skips duplicate rows."""
    cfg = config.get_config()
    max_map_items = cfg["max_map_items"]
    sensor_sn = row["sensor_sn"]
    timestamp = datestr_to_timestamp(row["timestamp"])

    if sensor_sn not in sensor_map:
        sensor_map[sensor_sn] = OrderedDict()
    timestamp_set = sensor_map[sensor_sn]
    if timestamp in timestamp_set:
        logging.warning(
            f"[HOBO-log] {timestamp} for sensor: {sensor_sn} already stored"
        )
        return True
    else:
        timestamp_set[timestamp] = None  # don't need a key value
        if len(timestamp_set) > max_map_items:
            (old_timestamp, _) = timestamp_set.popitem(last=False)
            logging.debug(
                f"[HOBO-log] removing {timestamp} for sensor: {sensor_sn} from timestamp set"
            )
    return False


def hsds_write(items):
    """Writes HOBO data to HSDS service"""
    cfg = config.get_config()
    hsds_filename = cfg["hsds_filename"]
    logging.debug(f"[HOBO-log] Opening {hsds_filename} for writing with HSDS")
    measurement_types = get_measurement_types()

    count = len(items)
    if count == 0:
        logging.warning("[HOBO-log] hsds_write empty row list")
        return 0

    logging.info(f"[HOBO-log] HSDS-write: {count} rows")

    # Create a numpy array
    arr = np.zeros((count), dtype=dt_measurements)

    for i in range(count):
        item = items[i]
        logger_sn = item["logger_sn"]
        sensor_sn = item["sensor_sn"]
        data_type_id = item["data_type_id"]
        si_value = item["si_value"]
        sensor_measurement_type = item["sensor_measurement_type"]
        if sensor_measurement_type not in measurement_types:
            logging.warning(
                f"[HOBO-log] Unexpected sensor measurement_type: {sensor_measurement_type}"
            )
            sensor_measurement_type_value = 0
        else:
            sensor_measurement_type_value = measurement_types[sensor_measurement_type]
        si_value = item["si_value"]
        timestamp = datestr_to_timestamp(item["timestamp"])

        logging.debug(
            "[HOBO-log] HSDS-write: "
            +
            # fields
            f"logger_sn={logger_sn}, "
            + f"sensor_sn={sensor_sn}, "
            + f"data_type_id={data_type_id}, "
            + f"si_value={si_value}, "
            + f"measurement_type='{sensor_measurement_type}', "
            + f"measurement_type_value={sensor_measurement_type_value}, "
            + f"timestamp={timestamp}"
        )
        # Get row from numpy array
        row = arr[i]
        # Assign fields (numpy doesn't let you do this inplace)
        row["logger_sn"] = logger_sn.encode("ascii")
        row["sensor_sn"] = sensor_sn.encode("ascii")
        row["data_type_id"] = data_type_id
        row["si_value"] = si_value
        row["measurement_type"] = sensor_measurement_type_value
        row["timestamp"] = timestamp
        arr[i] = row

    # Update the HDF store
    with h5File(hsds_filename, mode="a") as f:
        # Get reference to the dataset
        dset = f["data"]
        next_row = dset.shape[0]
        logging.info(
            f"[HOBO-log] Current data table shape: {dset.shape[0]}, adding: {count}"
        )
        # Extend by num_rows
        dset.resize((next_row + count,))
        # Write array to extended area
        dset[next_row : next_row + count] = arr[...]
        # Update 'last_updated_data' field
        ts = int(time.time())
        f.attrs["last_updated_data"] = ts
    return count


#
# Apply metadata file
#
def metadata_update(filename, h):
    """Updates metadata fields in the HDF store."""
    fn = "[HOBO-metadata]"
    logging.debug(f"{fn}('{filename}')")
    if not os.path.isfile(filename):
        logging.warning(f"[HOBO-metadata] YAML file: {filename} not found, ignoring")
        return 0
    with open(filename, "r") as f:
        yaml_config = None
        try:
            yaml_config = yaml.safe_load(f)
        except yaml.scanner.ScannerError as se:
            logging.error(
                f"[HOBO-metadata] {fn} Error loading YAML file: {filename}: {se}"
            )
            return 0
        count = 0
        if yaml_config:
            if "schema" not in yaml_config:
                logging.warning(
                    f"[HOBO-metadata] {fn} No schema key found in {filename}, ignoring"
                )
            else:
                # ts = np.uint32(datetime.utcnow().timestamp())
                schema = yaml_config["schema"]
                if schema == "hobo-general":
                    count = update_general(h, yaml_config)
                elif schema == "hobo-logger":
                    count = update_logger(h, yaml_config)
                elif schema == "hobo-sensor":
                    count = update_sensor(h, yaml_config)
                else:
                    logging.warning(
                        f"[HOBO-metadata] Unknown schema: {schema}, ignoring {filename}"
                    )
    return count


def metadata_sync_proc():
    """Syncs metadata in the HDF store with remote repository."""
    fn = "[HOBO-metadata-sync]"  # shorthand to reduce line length for log messages
    logging.info(fn)
    cfg = config.get_config()
    local_dir = cfg["meta_local_dir"]
    if not os.path.isdir(local_dir):
        logging.error(f"{fn} Filepath: {local_dir} not found, skipping metadata sync")
        return 0
    meta_repo = cfg["meta_repo"]
    logging.debug(f"{fn} Using metadata repo: {meta_repo}")
    index = meta_repo.rfind("/")
    if index < 0:
        logging.error(f"{fn} Unexpected name for metadata repository: {meta_repo}")
        return 0
    repo_name = meta_repo[(index + 1) :]
    logging.info(f"{fn} Metadata_sync repo name: {repo_name}")
    repo_dir = os.path.join(local_dir, repo_name)
    if not os.path.isdir(repo_dir):
        logging.info(f"{fn} repo_dir: {repo_dir} not found, cloning repo")
        # cd local_dir; git clone meta_repo
        shell_cmd = f"git clone --quiet {meta_repo} {repo_dir}"
    else:
        # do a git pull on the repo
        shell_cmd = f"cd {repo_dir}; git pull --quiet; cd -"

    rc = os.system(shell_cmd)
    if rc != 0:
        logging.error(f"{fn} shell command: {shell_cmd} failed")
        return 0

    count = 0
    hsds_filename = cfg["hsds_filename"]
    yml_paths = []
    yml_paths.append(
        os.path.join(repo_dir, cfg["meta_root_path"])
    )  # root metadata yaml file
    loggers_dir = os.path.join(repo_dir, cfg["meta_loggers_dir"])  # loggers dir
    if os.path.isdir(loggers_dir):
        for filename in os.listdir(loggers_dir):
            yml_paths.append(os.path.join(loggers_dir, filename))
    sensors_dir = os.path.join(repo_dir, cfg["meta_sensors_dir"])  # sensors dir
    if os.path.isdir(sensors_dir):
        for filename in os.listdir(sensors_dir):
            yml_paths.append(os.path.join(sensors_dir, filename))
    logging.info(f"{fn} Found {len(yml_paths)} YAML files")

    with h5File(hsds_filename, mode="a") as h:
        for yml_path in yml_paths:
            count += metadata_update(yml_path, h)

        if count > 0:
            logging.info(f"{fn} {count} updates, setting last_updated_metadata")
            if "last_updated_metadata" in h.attrs:
                del h.attrs["last_updated_metadata"]
            ts = np.uint32(datetime.utcnow().timestamp())
            h.attrs["last_updated_metadata"] = ts

    return count


def logger_data_proc(logger_index):
    """Run HOBO API query for a given logger."""

    cfg = config.get_config()
    loggers = get_loggers()

    logger = loggers[logger_index]
    logger_sn = logger["sn"].decode("utf-8")
    logging.info(f"[HOBO-log] Logger: {logger_sn}")

    max_api_time_delta = cfg["max_api_time_delta_minutes"]

    # Compare last_time timestamp against start and end datetime:
    # To avoid writing duplicate data in the HDF store
    last_query = get_logger_last_query(logger_index)

    end_date_time_cfg = cfg["end_date_time"]
    if end_date_time_cfg:
        logging.debug(f"[HOBO-log] using end_date_time: {end_date_time_cfg}")
        end_date_time = get_datetime(end_date_time_cfg)
        if end_date_time > datetime.utcnow():
            logging.warning("[HOBO-log] end_date_time is in the future: setting to now")
            end_date_time = datetime.utcnow()
    else:
        end_date_time = datetime.utcnow()

    start_date_time_cfg = cfg["start_date_time"]
    if start_date_time_cfg:
        start_date_time = get_datetime(start_date_time_cfg)
        if start_date_time > datetime.utcnow():
            logging.warning(
                "[HOBO-log] start_date_time is in the future, returning 0 rows"
            )
            return 0
    else:
        polling_time = cfg["polling_interval"]
        start_date_time = datetime.utcnow() - timedelta(minutes=polling_time)

    if last_query and last_query > start_date_time:
        start_date_time = last_query
        logging.debug(
            f"[HOBO-log] Re-set start_time based on last_query for logger: {logger_sn}"
        )

    if start_date_time + timedelta(minutes=max_api_time_delta) < end_date_time:
        logging.debug(
            f"[HOBO-log] adjusting end_date_time to be {max_api_time_delta} minutes ahead of start_date_time"
        )
        end_date_time = start_date_time + timedelta(minutes=max_api_time_delta)

    if start_date_time >= end_date_time:
        logging.warning(
            "[HOBO-log] start_date_time >= end_date_time, returning 0 items"
        )
        return 0
    logging.info(
        f"[HOBO-log] start_date_time: {start_date_time} end_date_time: {end_date_time}"
    )

    update_count = 0  # number of rows written
    update_rows = []
    max_results = True

    while max_results:
        rsp = api_query(
            logger_sn, start_date_time=start_date_time, end_date_time=end_date_time
        )
        if not rsp:
            logging.error("[HOBO-log] No response returned from api_query")
            break

        if "observation_list" not in rsp:
            logging.info("[HOBO-log] get_logger_values - observation_list not returned")
            logging.debug(f"[HOBO-log] get_logger_values - api_query response: {rsp}")
            break

        observation_list = rsp["observation_list"]
        if len(observation_list) == 0:
            logging.info(
                "[HOBO-log] get_logger_values - no rows found in observation_list"
            )
            break
        logging.info(f"[HOBO-log] get_logger_values - got {len(observation_list)} rows")

        if rsp["max_results"] == False:
            max_results = False

        last_timestamp = None

        for row in observation_list:
            timestamp = row["timestamp"]
            last_timestamp = get_datetime(timestamp)
            if last_timestamp >= end_date_time:
                msg = f"[HOBO-log] timestamp: {last_timestamp} >= "
                msg += "end_date_time, stop row iteration"
                logging.debug(msg)
                break

            if is_duplicate(row):
                logging.debug("[HOBO-log] skip duplicate")
            else:
                update_rows.append(row)

        start_date_time = last_timestamp
        msg = "[HOBO-log] get_logger_values - start_date_time next: "
        msg += f"{start_date_time}"
        logging.debug(msg)

        if end_date_time is not None and start_date_time >= end_date_time:
            max_results = False

    if len(update_rows) > 0:
        update_count = hsds_write(update_rows)

    if update_count == 0:
        update_logger_last_query(logger_index, end_date_time)

    if update_count > 0:
        update_logger_last_query(logger_index, last_timestamp)

    if update_count >= cfg["max_api_query_items"]:
        logging.warning(f"[HOBO-log] max_api_query_items limit reached: {update_count}")

    logging.info(f"[HOBO-log] data processing completed, {update_count} rows added")

    return update_count


#
# Main
#
def main():
    #
    # Setup log level
    #
    if "LOG_LEVEL" in os.environ:
        log_level = os.environ["LOG_LEVEL"]
    else:
        log_level = "DEBUG"

    print("[HOBO-log] Set-up log_level:", log_level)
    if log_level == "DEBUG":
        print("[HOBO-log] Starting debug")
        level = logging.DEBUG
    elif log_level == "INFO":
        level = logging.INFO
    elif log_level in ("WARN", "WARNING"):
        level = logging.WARNING
    elif log_level == "ERROR":
        level = logging.ERROR
    else:
        print(f"[HOBO-log] Unexpected log_level settings: {log_level}, defaulting to DEBUG")
        level = logging.DEBUG

    # logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s', level=level)
    logging.basicConfig(level=level)

    #
    # Define sleep time between queries
    # If polling_time was defined
    #
    cfg = config.get_config()
    polling_time = cfg["polling_interval"]
    metadata_last_sync = datetime.utcfromtimestamp(0)

    while True:
        count = 0
        if polling_time is not None and polling_time > 0:
            if datetime.utcnow() - timedelta(minutes=polling_time) > metadata_last_sync:
                # sync metadata from git repo
                count = metadata_sync_proc()
                logging.info(f"[HOBO-log] Got {count} metadata updates")
                metadata_last_sync = datetime.utcnow()

        loggers = get_loggers()
        num_loggers = len(loggers)
        if num_loggers == 0:
            logging.warning("[HOBO-log] No loggers defined, check your conf file")
            break

        count = 0
        for logger_index in range(num_loggers):
            count += logger_data_proc(logger_index)

        if count == 0:
            if polling_time is None:
                break
            logging.info(f"[HOBO-log] Sleeping for {polling_time} minutes")
            time.sleep(polling_time * 60)

    logging.info("[HOBO-log] Done: exiting")

#
# Main
#
main()
