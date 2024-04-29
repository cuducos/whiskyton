from flask import Flask
from flask_assets import Environment
from flask_migrate import Migrate

from whiskyton.assets import BUNDLES
from whiskyton.blueprints.files import files
from whiskyton.managers.charts import charts
from whiskyton.blueprints.site import site
from whiskyton.models import db


def create_app():
    # init whiskyton
    app = Flask("whiskyton")
    app.config.from_object("config")
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False

    # init db and migration manager
    db.init_app(app)
    Migrate(app, db)

    # scss
    assets = Environment(app)
    assets.load_path = [app.config["BASEDIR"] / "whiskyton"]
    for name, bundle in BUNDLES.items():
        assets.register(name, bundle)

    # register blueprints
    app.register_blueprint(site)
    app.register_blueprint(files)
    app.register_blueprint(charts, cli_group='charts')

    return app
