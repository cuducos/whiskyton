# coding: utf-8

from flask import Flask
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.assets import Environment, Bundle

# init whiskyton and db
app = Flask('whiskyton')
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from whiskyton import views, models

# scss
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle(
    'scss/search.scss',
    'scss/whisky_card.scss',
    'scss/footer.scss',
    'scss/autocomplete.scss',
    filters='pyscss',
    output='css/style.css')
assets.register('scss_style', scss)

# compressed js
js = Bundle(
    'js/jquery.autocomplete.js',
    'js/init.js',
    filters='rjsmin',
    output='js/init.min.js')
assets.register('js_init', js)
