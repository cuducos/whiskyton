from flask import Flask

from whiskyton.blueprints.files import files
from whiskyton.blueprints.site import site


def create_app():
    app = Flask("whiskyton")
    app.config.from_object("whiskyton.config")
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.register_blueprint(site)
    app.register_blueprint(files)
    return app
