#!venv/bin/python
import inspect
import os

current_file = os.path.abspath(inspect.getfile(inspect.currentframe()))
basedir = os.path.dirname(current_file)
charts_dir = basedir + '/whiskyton/static/charts/'
try:
    os.stat(charts_dir)
except:
    os.mkdir(charts_dir)
for filename in os.listdir(charts_dir):
    filepath = charts_dir + filename
    if os.path.isfile(filepath):
        os.remove(filepath)
