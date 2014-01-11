import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/whiskyton' 
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
MAIN_TITLE = 'Whiskyton'
HEADLINE = 'Find whiskies that you like!'
