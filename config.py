from unipath import Path
from decouple import config

BASEDIR = Path(__file__).parent
GOOGLE_ANALYTICS = config('GOOGLE_ANALYTICS', default=True, cast=bool)
SQLALCHEMY_DATABASE_URI = config('DATABASE_URL',
                                 default='sqlite:///' + BASEDIR.child('app.db'))
DEBUG = config('DEBUG', default=False, cast=bool)

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
