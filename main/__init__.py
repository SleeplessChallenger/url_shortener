from flask import Flask
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from main.config import config
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=config['production']):
	app = Flask(__name__)
	app.config.from_object(config_class)

	db.init_app(app)
	migrate.init_app(app, db)

	from main.routes import url
	from main.errors.handlers import err
	app.register_blueprint(url)
	app.register_blueprint(err)

	from .api import api as url_api
	app.register_blueprint(url_api, url_prefix='/api')

	return app
