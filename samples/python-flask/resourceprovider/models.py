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

import datetime
from flask import url_for, current_app
from resourceprovider import db
from xmlbuilder import XMLBuilder

app = current_app

class Subscription(db.Model):
	id             				= db.Column(db.String(128), primary_key=True)
	created_date				= db.Column(db.DateTime)
	state                       = db.Column(db.Integer)

class Event(db.Model):
	id 							= db.Column(db.Integer, primary_key=True)
	entity_state				= db.Column(db.String(128))
	subscription_creation_date	= db.Column(db.DateTime)
	operation_id				= db.Column(db.String(128))
	resource_type				= db.Column(db.String(128))
	email						= db.Column(db.String(128))
	opt_in						= db.Column(db.Boolean)
	subscription_id             = db.Column(db.String(128), db.ForeignKey('subscription.id'))
	subscription                = db.relationship('Subscription', backref=db.backref('events'), lazy='dynamic')

class CloudService(db.Model):
	id 							= db.Column(db.Integer, primary_key=True)
	name						= db.Column(db.String(128))
	geo_region					= db.Column(db.String(128))
	subscription_id             = db.Column(db.String(128), db.ForeignKey('subscription.id'))
	subscription                = db.relationship('Subscription', backref=db.backref('cloudservices'), lazy='dynamic')

	def to_xml(self):
		resources = self.resources
		x = XMLBuilder('CloudService', xmlns="http://schemas.microsoft.com/windowsazure")
		x['xml_header'] = True
		x.GeoRegion(self.geo_region)
		with x.Resources:
			for resource in self.resources:
				with x.Resource:
					x.ETag(resource.incarnation_id)
					x.Name(resource.name)
					with x.OperationStatus:
						x.Result("Succeeded")
					x.Plan(resource.plan)
					x.State("Started")
					x.SubState("Ready to go")
					x.Type(resource.resource_type)
					with x.UsageMeters:
						for usage_meter in resource.usage_meters:
							with x.UsageMeter:
								x.Included(usage_meter["Included"])
								x.Name(usage_meter["Name"])
								x.Unit(usage_meter["Unit"])
								x.Used(usage_meter["Used"])

		return str(x)

class Resource(db.Model):
	id 							= db.Column(db.Integer, primary_key=True)
	name						= db.Column(db.String(128))
	cloudservice_id             = db.Column(db.Integer, db.ForeignKey('cloud_service.id'))
	cloudservice                = db.relationship('CloudService', backref=db.backref('resources'), lazy='dynamic')
	resource_type				= db.Column(db.String(128))
	incarnation_id				= db.Column(db.String(128))
	schema_version				= db.Column(db.String(128))
	plan						= db.Column(db.String(128))
	version						= db.Column(db.String(128))
	intrinsic_settings 			= db.Column(db.Text)
	promotion_code				= db.Column(db.String(128))
	state 						= "Started"
	sub_state                   = "Ready to go"
	output_items                = { "key": "hardcoded_key", "password": "hardcoded_password" }
	usage_meters				= [
									{"Included": "20", "Name": "Connections", "Unit": "generic", "Used":"5"},
									{"Included": "1073741824", "Name": "Storage", "Unit": "bytes", "Used":"1181116006"}
								  ]

	def to_xml(self):
		x = XMLBuilder('Resource', xmlns="http://schemas.microsoft.com/windowsazure")
		x.CloudServiceSettings()
		x.ETag(self.incarnation_id)
		x.IntrinsicSettings()
		x.Name(self.name)

		with x.OperationStatus:
			x.Result("Succeeded")
		with x.OutputItems:
			for key in self.output_items.keys():
				with x.OutputItem:
					x.Key(key)
					x.Value(self.output_items[key])
		x.Plan(self.plan)
		x.State(self.state)
		x.SubState(self.sub_state)

		with x.UsageMeters:
			for usage_meter in self.usage_meters:
				with x.UsageMeter:
					x.Included(usage_meter["Included"])
					x.Name(usage_meter["Name"])
					x.Unit(usage_meter["Unit"])
					x.Used(usage_meter["Used"])

		x.Type(self.resource_type)
		return str(x)