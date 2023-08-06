from typing import Tuple


LOGRECORD_KEYS = [
    "name",
    "msg",
    "args",
    "levelname",
    "levelno",
    "pathname",
    "filename",
    "module",
    "exc_info",
    "exc_text",
    "stack_info",
    "lineno",
    "funcName",
    "created",
    "msecs",
    "relativeCreated",
    "thread",
    "threadName",
    "processName",
    "process",
]


def separate_log_data(log_data: dict) -> Tuple[dict, dict]:
    """Separate log data into main data and extra data."""

    main_data: dict = dict()
    extra_data: dict = dict()

    # loop over the keys, adding the values to the respective dictionaries
    for key in log_data.keys():
        if key in LOGRECORD_KEYS:
            main_data[key] = log_data[key]
        else:
            extra_data[key] = log_data[key]

    return main_data, extra_data
