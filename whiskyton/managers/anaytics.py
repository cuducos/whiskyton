from csv import writer
from datetime import datetime
from flask_script import Manager
from ftplib import FTP, error_perm
from tempfile import mkstemp
from whiskyton import app
from whiskyton.models import Whisky

AnalyticsCommand = Manager(usage='Save page views data via FTP')


@AnalyticsCommand.command
def save():
    """ Save a CSV with the number of page views of each whisky """

    # check if FTP settings are set & connect
    for i in ['server', 'user', 'password']:
        if not app.config['FTP_{}'.format(i.upper())]:
            print('==> Error: no FTP {} set'.format(i))
            return None
    try:
        ftp = FTP(app.config['FTP_SERVER'],
                  app.config['FTP_USER'],
                  app.config['FTP_PASSWORD'])
    except error_perm:
        info = '{}:{}@{}'.format(app.config['FTP_USER'],
                                 '*' * len(app.config['FTP_PASSWORD']),
                                 app.config['FTP_SERVER'])
        print("==> Couldn't connect to {}".format(info))
        return False

    # create a tmp csv
    timestamp = datetime.now().strftime('%Y%m%d')
    temp_file = mkstemp()
    with open(temp_file[1], 'w') as file_handler:
        csv = writer(file_handler)
        query = Whisky.query.all()
        data = list()
        for w in query:
            data.append([timestamp, w.id, w.slug, w.distillery, w.views])
        headers = ['date', 'id', 'slug', 'distillery', 'views']
        csv.writerows([headers] + data)

    # save file
    if app.debug:
        file_name = 'debug-{}.csv'.format(timestamp)
    else:
        file_name = 'analytics-{}.csv'.format(timestamp)
    if not ftp.storlines('STOR {}'.format(file_name), open(temp_file[1], 'r')):
        print("==> FTP error while saving the file")
        return False
    print('==> Saved as {} at {}'.format(file_name, app.config['FTP_SERVER']))
    return True
