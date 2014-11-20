# coding: utf-8

from flask import Flask
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.assets import Environment, Bundle

# init whiskyton and db
app = Flask('whiskyton')
app.config.from_object('config')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from whiskyton import views, models

# add commands to manage chart cache
from charts_manager import ChartsCommand
manager.add_command('charts', ChartsCommand)

# scss
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle(
    'scss/header.scss',
    'scss/search.scss',
    'scss/whisky_card.scss',
    'scss/footer.scss',
    'scss/autocomplete.scss',
    filters='pyscss, cssmin',
    output='css/style.css')
assets.register('scss_style', scss)

# compressed js
js = Bundle(
    'js/jquery.autocomplete.js',
    Bundle('coffeescript/init.coffee', filters='coffeescript'),
    filters='rjsmin',
    output='js/init.min.js')
assets.register('js_init', js)
