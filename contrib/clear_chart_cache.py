# coding: utf-8
from unipath import Path

base_dir = Path().parent
charts_dir = base_dir.child('whiskyton', 'static', 'charts').absolute()
files = charts_dir.listdir()
for f in files:
    f.remove()
