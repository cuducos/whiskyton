from flask import Flask

from whiskyton.blueprint import site


def create_app():
    app = Flask("whiskyton")
    app.config.from_object("whiskyton.config")
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.register_blueprint(site)
    return app
