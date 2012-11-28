from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from resourceprovider import settings

db = SQLAlchemy()
app = Flask(__name__)

def create_app(env=None):
	config = {
		"SQLALCHEMY_DATABASE_URI": "mysql://%s:%s@%s/%s" % (
			settings.database["prod"]["user"],
			settings.database["prod"]["password"],
			settings.database["prod"]["host"],
			settings.database["prod"]["database"],
			),
	}

	if env == "test":
		config = {
		"SQLALCHEMY_DATABASE_URI": "mysql://%s:%s@%s/%s" % (
			settings.database["test"]["user"],
			settings.database["test"]["password"],
			settings.database["test"]["host"],
			settings.database["test"]["database"],
			),
		}

	app.config.update(config)
	db.init_app(app)
	return app

import general
app.register_blueprint(general.mod)

if __name__ == "main":
	app.logger.debug("Entered main method in /resourceprovider/__init__.py")
	app = create_app("production")
	app.run()
else:
	create_app("production")