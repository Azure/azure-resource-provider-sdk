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

import os
import unittest
import tempfile
import sqlalchemy
import requests
import envoy
import resourceprovider
import time
import untangle
import urllib
import xmlutil, settings
from flask.ext.sqlalchemy import SQLAlchemy
from resourceprovider import settings

class ResourceProviderTestCase(unittest.TestCase):
	def setUp(self):
		self.test_config = {
			"connection_uri": settings.dev["connection_uri"],
			"subscription_id": "1",
			"cloud_service_name": "mycloudservice",
			"resource_type": "cloudkeys",
			"resource_name": "mycloudkeysresource"
		}

		self.db_uri = "mysql://%s:%s@%s" % (
				settings.database["test"]["user"],
				settings.database["test"]["password"],
				settings.database["test"]["host"]				
			)
		self.engine = sqlalchemy.create_engine(self.db_uri) # connect to server
		self.engine.execute("DROP DATABASE IF EXISTS %s" % settings.database["test"]["database"]) #create db
		self.engine.execute("CREATE DATABASE %s" % settings.database["test"]["database"]) #create db
		self.engine.execute("USE %s" % settings.database["test"]["database"]) # select new db
		resourceprovider.app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://%s:%s@%s/%s" % (
			settings.database["test"]["user"],
			settings.database["test"]["password"],
			settings.database["test"]["host"],
			settings.database["test"]["database"],
			)
		with resourceprovider.app.test_request_context():
			resourceprovider.db.create_all(app=resourceprovider.create_app(env="test"))

	def do_register_subscription(self):
		xml = xmlutil.xml_for_subscription_event(self.test_config["subscription_id"], "Registered")
		result = requests.post("%s/subscriptions/%s/Events" % (
				self.test_config["connection_uri"],
				self.test_config["subscription_id"]),
			xml)
		return result

	def do_create_resource(self):
		xml = xmlutil.xml_for_create_resource(promotion_code="SomeCode",intrinsic_settings="")
		result = requests.put("%s/subscriptions/%s/cloudservices/%s/resources/%s/%s" % (
			self.test_config["connection_uri"],
			self.test_config["subscription_id"],			
			self.test_config["cloud_service_name"],
			self.test_config["resource_type"],
			self.test_config["resource_name"]), xml)
		return result

	def tearDown(self):
		self.engine.execute("DROP DATABASE IF EXISTS resourceprovidertest")

	# ======== Unit Tests ========
	def test_create_resource_fails_on_subscription_that_has_not_been_enabled(self):
		xml = xmlutil.xml_for_create_resource(promotion_code="SomeCode",intrinsic_settings="")
		result = requests.post("http://0.0.0.0:5000/subscriptions/%s/cloudservices/%s/resources/%s/%s" % ("2", "mycloudservice", "cloudkeys", "foobar"), xml)
		assert result.status_code == 404

	def test_register_subscription(self):
		result = self.do_register_subscription()
		assert result.status_code == 200

	def test_create_resource_succeeds_on_subscription_that_has_been_enabled(self):
		registration_result = self.do_register_subscription()
		create_result = self.do_create_resource()
		assert create_result.status_code == 200

	def test_get_cloud_service(self):
		registration_result = self.do_register_subscription()
		create_result = self.do_create_resource()
 		get_cloud_service_result = 	requests.get("%s/subscriptions/%s/cloudservices/%s" % (
 			self.test_config["connection_uri"],
 			self.test_config["subscription_id"], 
 			self.test_config["cloud_service_name"]
 			)
 		)
		assert get_cloud_service_result.status_code == 200

	def test_get_resource(self):
		registration_result = self.do_register_subscription()
		create_result = self.do_create_resource()
		get_resource_result = requests.get("%s/subscriptions/%s/cloudservices/%s/resources/%s/%s" % (
 			self.test_config["connection_uri"],
 			self.test_config["subscription_id"], 
 			self.test_config["cloud_service_name"],
 			self.test_config["resource_type"],
 			self.test_config["resource_name"]
 			)
 		)
		assert get_resource_result.status_code == 200

	def test_delete_resource(self):
		registration_result = self.do_register_subscription()
		create_result = self.do_create_resource()
		delete_resource_result = requests.delete("%s/subscriptions/%s/cloudservices/%s/resources/%s/%s" % (
 			self.test_config["connection_uri"],
 			self.test_config["subscription_id"], 
 			self.test_config["cloud_service_name"],
 			self.test_config["resource_type"],
 			self.test_config["resource_name"]
 			)
 		)
		assert delete_resource_result.status_code == 200

	def test_delete_cloud_service(self):
		registration_result = self.do_register_subscription()
		create_result = self.do_create_resource()
		delete_cloud_service_result = requests.delete("%s/subscriptions/%s/cloudservices/%s" % (
 			self.test_config["connection_uri"],
 			self.test_config["subscription_id"], 
 			self.test_config["cloud_service_name"]
 			)
 		)
		assert delete_cloud_service_result.status_code == 200

	def test_sso(self):
		registration_result = self.do_register_subscription()
		create_result = self.do_create_resource()		
		sso_token_result = requests.post("%s/subscriptions/%s/cloudservices/%s/resources/%s/%s/SsoToken" % (
 			self.test_config["connection_uri"],
 			self.test_config["subscription_id"], 
 			self.test_config["cloud_service_name"],
  			self.test_config["resource_type"],
 			self.test_config["resource_name"]			
 			)
 		)
 		message = untangle.parse(sso_token_result.text)

 		assert sso_token_result.status_code == 200 
 		assert message.SsoToken.TimeStamp.cdata is not None 	#todo: should actually check timestamp is a real timestamp
 		assert message.SsoToken.Token.cdata is not None

 		fragment = urllib.urlencode(
 			{
 				"token": message.SsoToken.Token.cdata,
 				"timestamp": message.SsoToken.TimeStamp.cdata
 			}
 		)

 		sso_view_result = requests.get("%s/sso?subid=%s&cloudservicename=%s&resourcetype=%s&resourcename=%s&%s" % (
 			self.test_config["connection_uri"],
 			self.test_config["subscription_id"], 
 			self.test_config["cloud_service_name"],
  			self.test_config["resource_type"],
 			self.test_config["resource_name"],
 			fragment
 			)
 		)

 		assert sso_view_result.status_code == 200
 		assert "Welcome" in sso_view_result.text

if __name__ == '__main__':
	unittest.main()