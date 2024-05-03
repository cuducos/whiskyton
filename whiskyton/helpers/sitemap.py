from datetime import datetime
from pathlib import Path

from flask import current_app


def recursive_listdir(path):
    """
    Lists recursively all files inside a given directory and its subdirectories
    :param path: (pathlib.Path or string) path to the directory
    :return: (list of pathlib.Path) list containing the path to all the files
        inside the given directory
    """
    folder = Path(path)
    files = list()
    for f in folder.glob("**/*"):
        if not f.is_file():
            continue
        files.append(f.absolute())
    return files


def most_recent_update(dir=None):
    """
    Returns the date of the most recent file update within the app.
    :return: (string) date in the format YYYY-MM-DD
    """
    dir = dir or current_app.config["BASEDIR"] / "whiskyton"
    files = recursive_listdir(dir)
    last_change = 0
    for f in files:
        f_last_change = f.stat().st_atime
        if f_last_change > last_change:
            last_change = f_last_change
    return datetime.fromtimestamp(last_change).strftime("%Y-%m-%d")
