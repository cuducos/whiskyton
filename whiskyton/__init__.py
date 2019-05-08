import logging
from flask import Flask
from flask_assets import Environment
from flask_compress import Compress
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from logging import StreamHandler

# init whiskyton
app = Flask('whiskyton')
app.config.from_object('config')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


# init db and migration manager
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# add commands to manage chart cache
from whiskyton.managers.charts import ChartsCommand
manager.add_command('charts', ChartsCommand)

# add command to save analytics data via FTP
from whiskyton.managers.anaytics import AnalyticsCommand
manager.add_command('analytics', AnalyticsCommand)

# enable gzip compression
Compress(app)

# scss
assets = Environment(app)
assets.load_path = [app.config['BASEDIR'].child('whiskyton')]
assets.from_yaml(app.config['BASEDIR'].child('whiskyton', 'assets.yaml'))

# register blueprints
from whiskyton.blueprints.site import site
from whiskyton.blueprints.files import files
app.register_blueprint(site)
app.register_blueprint(files)

# log errors
log_handler = StreamHandler()
app.logger.setLevel(logging.DEBUG)
app.logger.addHandler(log_handler)
