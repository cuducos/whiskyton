# coding: utf-8

from datetime import datetime
from unipath import Path
from whiskyton import app


def recursive_listdir(path):
    folder = Path(path)
    files = []
    for f in folder.listdir():
        if f.isdir():
            files.extend(recursive_listdir(f))
        else:
            files.append(f.absolute())
    return files


def most_recent_update():
    files = recursive_listdir(app.config['BASEDIR'].child('whiskyton'))
    last_change = 0
    for f in files:
        f_last_change = Path(f).atime()
        if f_last_change > last_change:
            last_change = f_last_change
    return datetime.fromtimestamp(last_change).strftime('%Y-%m-%d')
