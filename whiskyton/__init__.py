from flask import Flask
from flask_migrate import Migrate

from whiskyton.blueprints.files import files
from whiskyton.blueprints.site import site
from whiskyton.managers.charts import charts
from whiskyton.models import db


def create_app():
    # init whiskyton
    app = Flask("whiskyton")
    app.config.from_object("config")
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    # init db and migration manager
    db.init_app(app)
    Migrate(app, db)

    # register blueprints
    app.register_blueprint(site)
    app.register_blueprint(files)
    app.register_blueprint(charts, cli_group="charts")

    return app
