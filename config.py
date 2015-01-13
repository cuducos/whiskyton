# coding: utf-8
from unipath import Path
from decouple import config

BASEDIR = Path(__file__).parent
GOOGLE_ANALYTICS = config('GOOGLE_ANALYTICS', default=True, cast=bool)
default_db = 'sqlite:///' + BASEDIR.child('app.db')
SQLALCHEMY_DATABASE_URI = config('DATABASE_URL', default=default_db)
DEBUG = config('DEBUG', default=False, cast=bool)

FTP_SERVER = config('FTP_SERVER', default=False)
FTP_USER = config('FTP_USER', default=False)
FTP_PASSWORD = config('FTP_PASSWORD', default=False)

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
    'winey'
)
