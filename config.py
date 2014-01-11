import os
basedir = os.path.abspath(os.path.dirname(__file__))
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    GOOGLE_ANALYTICS = False
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    GOOGLE_ANALYTICS = True
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
MAIN_TITLE = 'Whiskyton'
HEADLINE = 'Find whiskies that you like!'
