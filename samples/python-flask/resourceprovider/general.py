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

from flask import Blueprint, request, flash, redirect, render_template, url_for, current_app, session, Response, abort
from flask.views import MethodView
from resourceprovider.models import Subscription, Event, CloudService, Resource
from resourceprovider import app, db
from datetime import datetime
from xmlbuilder import XMLBuilder
import untangle
import hashlib
import iso8601
from decorators import log_request_body

mod = Blueprint('general', __name__)
app.debug = True

sso_secret = 'some_massive_secret'

# GET https:// <registered-resource-provider-endpoint>/ subscriptions/{subscriptionId}/cloudservices/{cloud-service-name}/
@app.route('/subscriptions/<subscription_id>/cloudservices/<cloud_service_name>', methods=['GET'])
@log_request_body
def get_cloudservice(subscription_id, cloud_service_name):
	subscription = Subscription.query.filter_by(id=subscription_id).first()
	if not subscription:
		app.logger.debug("Subscription ID %s not found" % subscription_id)
		abort(404)

	cloud_service = CloudService.query.filter_by(subscription_id=subscription_id).first()
	if not cloud_service:
		app.logger.debug("Cloud Service with subscription ID %s not found" % subscription_id)
		abort(404)

	response_string = cloud_service.to_xml()
	app.logger.debug(response_string)
	return Response(response_string, status=200, mimetype='text/xml')

#           /subscriptions/<subscription_id>/cloudservices/<cloud_service_name>/resources/<resource_type>/<resource_name>/SsoToken
@app.route("/subscriptions/<subscription_id>/cloudservices/<cloud_service_name>/resources/<resource_type>/<resource_name>/SsoToken", methods=['POST'])
@log_request_body
def sso_token(subscription_id, cloud_service_name, resource_type, resource_name):
	signature = "%s:%s:%s:%s" % (subscription_id, cloud_service_name, resource_name, sso_secret)
	token = hashlib.sha1(signature)
	timestamp = str(datetime.now())

	x = XMLBuilder('SsoToken', xmlns='http://schemas.microsoft.com/windowsazure')
	x.TimeStamp(timestamp)
	x.Token(str(token.hexdigest()))

	response_string = str(x)
	app.logger.debug(response_string)
	return Response(response_string, status=200, mimetype='text/xml')

@app.route("/sso", methods=['GET'])
@log_request_body
def sso_view():
	subscription_id = request.args.get("subid")
	cloud_service_name = request.args.get("cloudservicename")
	resource_name = request.args.get("resourcename")
	timestamp = request.args.get("timestamp")

	for key,value in request.args.items():
		app.logger.debug("%s/%s" % (key,value))

	signature = "%s:%s:%s:%s" % (subscription_id, cloud_service_name, resource_name, sso_secret)
	token_now = str(hashlib.sha1(signature).hexdigest())
	if (token_now == request.args.get("token")):
		app.logger.debug("Tokens match, checking timestamp")
		timestamp_now = datetime.now()
		timestamp_given = iso8601.parse_date(timestamp).replace(tzinfo=None)
		time_delta = timestamp_now - timestamp_given
		if(time_delta.seconds < 60*10):
			return "Welcome you are logged in"
		else:
			app.logger.debug("SSO error: Time delta greater 10 minutes")
			return "Not logged in. Time delta > 10 minutes. Given: %s, now: %s" % (str(timestamp_given), str(timestamp_now))
	else:
		app.logger.debug("SSO error: Given token %s does not match required token %s" % (request.args.get("token"), token_now))
		return "Not logged in. Token mismatch."

@app.route("/subscriptions/<subscription_id>/cloudservices/<cloud_service_name>/resources/<resource_type>/<resource_name>", methods=['PUT'])
@log_request_body
def create_resource(subscription_id, cloud_service_name, resource_type, resource_name):
	message = untangle.parse(request.data)

	cloud_service = CloudService.query.filter_by(name=cloud_service_name,subscription_id=subscription_id).first()
	if not cloud_service:
		cloud_service = CloudService()
		cloud_service.name = cloud_service_name
		cloud_service.geo_region = message.Resource.CloudServiceSettings.GeoRegion.cdata
		cloud_service.subscription_id = subscription_id
		db.session.add(cloud_service)
		db.session.commit()

	subscription = Subscription.query.filter_by(id=subscription_id).first()
	if not subscription:
		app.logger.debug("Subscription ID %s not found" % subscription_id)
		abort(404)

	resource = Resource()
	resource.name = resource_name
	resource.cloudservice_id = cloud_service.id
	resource.resource_type = resource_type
	resource.schema_version = message.Resource.SchemaVersion.cdata
	resource.plan = message.Resource.Plan.cdata
	resource.version = message.Resource.SchemaVersion.cdata
	try:
		resource.promo_code = message.Resource.PromotionCode
	except IndexError:
		app.logger.debug("Promotion code not found")

	resource.incarnation_id = message.Resource.ETag.cdata
	app.logger.debug("Saving resource %s" % resource_name)
	db.session.add(resource)
	db.session.commit()

	response_body = resource.to_xml()
	app.logger.debug(response_body)
	return Response(response_body, mimetype='text/xml')

# PUT   https:// <registered-resource-provider-endpoint>/ subscriptions/{subscriptionId}/cloudservices/{cloud-service-name}/Resources/{resource-type}/{resource-name}
@app.route("/subscriptions/<subscription_id>/cloudservices/<cloud_service_name>/resources/<resource_type>/<resource_name>", methods=['POST'])
@log_request_body
def update_resource(subscription_id, cloud_service_name, resource_type, resource_name):
	message = untangle.parse(request.data)

	subscription = Subscription.query.filter_by(id=subscription_id).first()
	cloud_service = CloudService.query.filter_by(name=cloud_service_name,subscription_id=subscription_id).first()

	if not subscription:
		app.logger.debug("Can't update subscription ID %s because it was not found" % subscription_id)
		abort(404)
	if not cloud_service:
		app.logger.debug("Can't update cloud service ID %s because it was not found" % cloudservice_id)
		abort(404)

	resource = Resource.query.filter_by(name=resource_name, cloudservice_id=cloud_service_name).first()

	resource.name = resource_name
	resource.cloudservice_id = cloud_service.id
	resource.resource_type = resource_type
	resource.schema_version = message.Resource.SchemaVersion.cdata
	resource.plan = message.Resource.Plan.cdata
	resource.version = message.Resource.SchemaVersion.cdata
	try:
		resource.promo_code = message.Resource.PromotionCode
	except IndexError:
		app.logger.debug("Promotion code not found")

	resource.incarnation_id = message.Resource.ETag.cdata
	app.logger.debug("Saving resource %s" % resource_name)
	db.session.add(resource)
	db.session.commit()

	response_body = resource.to_xml()

	app.logger.debug(response_body)
	return Response(response_body, status=200, mimetype='text/xml')

# GET	https:// <registered-resource-provider-endpoint>/ subscriptions/{subscriptionId}/cloudservices/{cloud-service-name}/Resources/{resource-type}/{resource-name}
@app.route("/subscriptions/<subscription_id>/cloudservices/<cloud_service_name>/resources/<resource_type>/<resource_name>", methods=['GET'])
@log_request_body
def get_resource(subscription_id, cloud_service_name, resource_type, resource_name):
	subscription = Subscription.query.filter_by(id=subscription_id).first()
	if not subscription:
		app.logger.debug("Subscription ID %s not found" % subscription_id)
		abort(404)

	cloud_service = CloudService.query.filter_by(name=cloud_service_name,subscription_id=subscription_id).first()
	if not cloud_service:
		app.logger.debug("Cloud Service with subscription ID %s not found" % subscription_id)
		abort(404)

	resource = Resource.query.filter_by(name=resource_name, cloudservice_id=cloud_service.id).first()
	if not resource:		
		app.logger.debug("Resource with name %s not found" % resource_name)

	response_body = resource.to_xml()
	app.logger.debug(response_body)
	return Response(response_body, status=200, mimetype='text/xml')

# DELETE	https:// <registered-resource-provider-endpoint>/ subscriptions/{subscriptionId}/cloudservices/{cloud-service-name}/
@app.route("/subscriptions/<subscription_id>/cloudservices/<cloud_service_name>", methods=['DELETE'])
@log_request_body
def delete_cloud_service(subscription_id, cloud_service_name):
	subscription = Subscription.query.filter_by(id=subscription_id).first()
	if not subscription:
		app.logger.debug("Subscription ID %s not found" % subscription_id)
		abort(404)

	cloud_service = CloudService.query.filter_by(name=cloud_service_name,subscription_id=subscription_id).first()
	if not cloud_service:
		app.logger.debug("Cloud Service with subscription ID %s not found" % subscription_id)
		abort(404)

	resources = Resource.query.filter_by(cloudservice_id=cloud_service.id)
	for resource in resources:
		db.session.delete(resource)

	db.session.commit()
	resp = Response(None, status=200, mimetype='application/xml')
	return resp


# DELETE	https://<registered-resource-provider-endpoint>/ subscriptions/{subscriptionId}/cloudservices/{cloud-service-name}/Resources/{resource-type}/{resource-name}
@app.route("/subscriptions/<subscription_id>/cloudservices/<cloud_service_name>/resources/<resource_type>/<resource_name>", methods=['DELETE'])
@log_request_body
def delete_resource(subscription_id, cloud_service_name, resource_type, resource_name):
	subscription = Subscription.query.filter_by(id=subscription_id).first()
	if not subscription:
		app.logger.debug("Subscription ID %s not found" % subscription_id)
		abort(404)

	cloud_service = CloudService.query.filter_by(name=cloud_service_name,subscription_id=subscription_id).first()
	if not cloud_service:
		app.logger.debug("Cloud Service with subscription ID %s not found" % subscription_id)
		abort(404)

	resource = Resource.query.filter_by(name=resource_name, cloudservice_id=cloud_service.id).first()
	if not resource:		
		app.logger.debug("Resource with name %s not found" % resource_name)

	db.session.delete(resource)
	db.session.commit()

	resp = Response(None, status=200, mimetype='application/xml')
	return resp

@app.route('/subscriptions/<subscription_id>/Events', methods=['POST'])
@log_request_body
def event(subscription_id):	
	message = untangle.parse(request.data)
	operation_id = message.EntityEvent.OperationId.cdata
	event = Event.query.filter_by(operation_id=operation_id).first()
	app.logger.debug("POST on /subscription/%s/events with body %s" % (subscription_id, request.data))

	event_time = iso8601.parse_date(message.EntityEvent.EntityId.Created.cdata)

	if event:
		app.logger.debug("Event ID %s already recorded, will not do anything" % operation_id)
		return Response(None, status=200, mimetype='application/xml')

	app.logger.debug("Creating a new event with parameters %s" % subscription_id)
	event = Event()
	event.subscription_id = subscription_id
	event.operation_id = message.EntityEvent.OperationId.cdata
	event.entity_state = message.EntityEvent.EntityState.cdata

	try:
		properties = message.EntityEvent.Properties
		for entity_property in properties.children:
			property_name = entity_property.PropertyName.cdata
			property_value = entity_property.PropertyValue.cdata
			if property_name == "ResourceType":
				event.resource_type = property_value
			elif property_name == "EMail":
				event.email = property_value
			elif property_name == "OptIn":
				if property_value == "True":
					event.opt_in = True
				elif property_value == "False":
					event.opt_in = False
				else:
					app.logger.debug("Unknown value %s for OptIn property" % property_value)
			else:
				app.logger.debug("Unknown property '%s' with value '%s' found" % (property_name, property_value))
	except IndexError:
		app.logger.debug("No properties received")

	if message.EntityEvent.EntityId:
		event.subscription_created_date = event_time
	app.logger.debug("Saving new event with operation_id %s" % event.operation_id)

	if event.entity_state == "Registered":
		app.logger.debug("Registered event for subscription ID %s, creating a subscription" % subscription_id)
		subscription = Subscription.query.filter_by(id=subscription_id).first()
		if not subscription:
			subscription = Subscription()
			subscription.state = 1 # registered
			subscription.id = subscription_id
			if message.EntityEvent.EntityId:
				subscription.created_date = event_time
			db.session.add(subscription)
			db.session.commit()
	else:
		app.logger.debug("Update event for subscription ID %s, updating state" % subscription_id)
		subscription = Subscription.query.filter_by(id=subscription_id).first()
		if not subscription:
			abort(404)
		if event.entity_state == "Disabled":
			subscription.state = 2
		elif event.entity_state == "Deleted":
			subscription.state = 3
		db.session.add(subscription)
		db.session.commit()

	db.session.add(event)
	db.session.commit()

	resp = Response(None, status=200, mimetype='application/xml')
	return resp
