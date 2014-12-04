# coding: utf-8

from datetime import datetime
from unipath import Path
from whiskyton import app


def recursive_listdir(path):
    """
    Lists recursively all files inside a given directory and its subdirectories.
    path: (unipath.Path or string) path to the directory
    return: (list of unipath.Path) list containing the path to all the files
        inside the given directory
    """
    folder = Path(path)
    files = []
    for f in folder.listdir():
        if f.isdir():
            files.extend(recursive_listdir(f))
        else:
            files.append(f.absolute())
    return files


def most_recent_update():
    """
    Returns the date of the most recent file update within the app.
    return: (string) date in the format YYYY-MM-DD
    """
    files = recursive_listdir(app.config['BASEDIR'].child('whiskyton'))
    last_change = 0
    for f in files:
        f_last_change = Path(f).atime()
        if f_last_change > last_change:
            last_change = f_last_change
    return datetime.fromtimestamp(last_change).strftime('%Y-%m-%d')
