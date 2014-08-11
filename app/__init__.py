from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.assets import Environment, Bundle

# init app and db
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
from app import views, models

# SCSS
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle(
    'scss/style.scss',
    'scss/typeahead.fix.scss',
    filters='pyscss',
    output='css/style.css')
assets.register('scss_style', scss)
