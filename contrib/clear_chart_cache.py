import os

charts_dir = '../whiskyton/static/charts/'
try:
    os.stat(charts_dir)
except:
    os.mkdir(charts_dir)
for filename in os.listdir(charts_dir):
    filepath = charts_dir + filename
    if os.path.isfile(filepath):
        os.remove(filepath)
