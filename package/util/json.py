"""Util file with json reading/writing functions.
"""

import json

from datetime import datetime

dateFormat = '%d %b %Y'


def _dateToStr(date: datetime):
    """Converts datetime to str.

    Args:
        date (datetime): Date to convert.

    Returns:
        A string representation of the date.
    """
    return date.strftime(dateFormat)


def _dateHook(json_dict: dict):
    """Converts str to datetime during json load.

    Args:
        json_dict (dict): dict.

    Returns:
        A dict with dates in the datetime class.
    """
    for key, value in json_dict.items():
        if key.endswith('date'):
            json_dict[key] = datetime.strptime(value, dateFormat)
        else:
            pass
    return json_dict


def openJson(file):
    """Opens a json file.

    Args:
        file: Opened file object.

    Returns:
        A dict, representing the json file content.
    """
    return json.load(file, object_hook=_dateHook)


def writeJson(file, json_dict: dict):
    """Writes to a json file.

    Args:
        file: File object of the file to write to.
        json_dict (dict): A dict, which to convert to json
    """
    json.dump(json_dict, file, indent=4, sort_keys=True, default=_dateToStr)
