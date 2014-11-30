# coding: utf-8

from flask import Flask
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.assets import Environment, Bundle

# init whiskyton
app = Flask('whiskyton')
app.config.from_object('config')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# init db
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# add commands to manage chart cache
from whiskyton.managers.charts import ChartsCommand
manager.add_command('charts', ChartsCommand)

# scss
assets = Environment(app)
assets.load_path = [
    app.config['BASEDIR'].child('whiskyton', 'coffeescript'),
    app.config['BASEDIR'].child('whiskyton', 'scss'),
    app.config['BASEDIR'].child('whiskyton', 'static', 'js')

]
scss = Bundle(
    'header.scss',
    'search.scss',
    'whisky_card.scss',
    'footer.scss',
    'autocomplete.scss',
    filters='pyscss, cssmin',
    output='css/style.css')
assets.register('scss_style', scss)

# compressed js
js = Bundle(
    'jquery.autocomplete.js',
    Bundle('init.coffee', filters='coffeescript'),
    filters='rjsmin',
    output='js/init.min.js')
assets.register('js_init', js)

# register blueprints
from whiskyton.blueprints.site import site_blueprint
from whiskyton.blueprints.files import files_blueprint
app.register_blueprint(site_blueprint)
app.register_blueprint(files_blueprint)
