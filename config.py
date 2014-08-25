import os
basedir = os.path.abspath(os.path.dirname(__file__))
if os.environ.get('DATABASE_URL') is None:
    local_db_uri = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = local_db_uri
    GOOGLE_ANALYTICS = False
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    GOOGLE_ANALYTICS = True
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
MAIN_TITLE = 'Whiskyton'
HEADLINE = 'Find whiskies that you like!'
TASTES = (
    'spicy',
    'honey',
    'tobacco',
    'medicinal',
    'smoky',
    'sweetness',
    'body',
    'floral',
    'fruity',
    'malty',
    'nutty',
    'winey')
