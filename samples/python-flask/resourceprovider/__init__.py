#
# Copyright 2011 Microsoft Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

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