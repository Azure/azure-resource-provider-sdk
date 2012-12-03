# manifest checks:
# - check if manifest contains test and production sections
# - check if test and production sections contain base and sso endpoints
# - check if test and production base and sso endpoints are https://
# - check if outputkeys are present
# - check that manifest doesn't contain xml header

# global -check alpha ordering [DONE]

# create
# - register subscription [DONE]
# - create resource on enabled [DONE]
# - check return values [DONE]
# - create resource on not enabled

# get
# - can get resource [DONE]
# - can get cloudservice [DONE]

# update
# - check that update plan from 1 to 2 works [DONE]
# - check that email can be updated

# disable is processed

# delete
# - check that resource can be deleted

# sso
# - sso with expired timestamp
# - sso with bad token

import re
import string
import urllib

from client import Client
from utility import Printer, generate_etag
from xmlutil import get_subtree_from_element, get_subtree_from_xml_string, get_namespace, get_root_tag, node_exists, get_node_value, get_nodes, xml_for_subscription_event, xml_for_create_resource

class Validator(object):
	def __init__(self,config):
		self.config = config

		env = self.config['env']
		self.client = Client(
			config['manifest'][env]['base'],
			config['manifest'][env]['sso']
			)

	def _check_node_exists(self, t, xpath, behavior="error"):
		try:
			node_exists(t, xpath)
		except NodeNotFoundException:
			msg = "XPath %s was not found in the response" % xpath
			if behavior == "error":
				Printer.error(msg)
			else:
				Printer.warn(msg)

	def _check_node_value(self, t, xpath, expected):
		try:
			actual = get_node_value(t, xpath)
			if actual != expected:
				Printer.error("Node at XPath %s has actual value %s, expected value %s" % (xpath, actual, expected))

		except NodeNotFoundException:
			Printer.error("Node at XPath %s was not found in the response" % xpath)

	def _validate_resource_response(self, etag, t):
		root_node_expected_tag = '{0}Resource'.format(get_namespace(t))
		root_node_actual_tag = get_root_tag(t)
		if (root_node_expected_tag != root_node_actual_tag):
			Printer.error("Root node does not have expected tag %s" % root_node_expected_tag)
		self._check_node_exists(t, './{0}CloudServiceSettings')
		self._check_node_value(t, './{0}ETag', etag)
		self._check_node_value(t, './{0}Name', self.config['resource_name'])
		self._check_node_value(t, './{0}OperationStatus/{0}Result', "Succeeded")
		if self._check_node_exists(t, './{0}OutputItems', behavior='warn'):
			output_items = t.findall('.//{0}OutputItem'.format(get_namespace(t)))
			for output_item in output_items:
				output_item_tree = get_subtree_from_element(output_item)
				self._check_node_exists(output_item_tree, './{0}Key')
				self._check_node_exists(output_item_tree, './{0}Value')

		if self._check_node_exists(t, './{0}UsageMeters', behavior='warn'):
			usage_meters = get_nodes('.//{0}UsageMeter')
			for usage_meter in usage_meters:
				usage_meter_tree = get_subtree_from_element(usage_meter)
				self._check_node_exists(usage_meter_tree, './{0}Included')
				self._check_node_exists(usage_meter_tree, './{0}Name')
				self._check_node_exists(usage_meter_tree, './{0}Unit', behavior='warn')
				self._check_node_exists(usage_meter_tree, './{0}Used')

		self._check_node_exists(t, './{0}Plan')
		self._check_node_value(t, './{0}State', "Started")		


	def get_resource(self):
		Printer.start_test("Get Resource")
		etag = generate_etag()

		(status, response) = self.client.perform_request(
				"subscriptions/%s/cloudservices/%s/resources/%s/%s" % (
					self.config["subscription_id"],
					self.config["cloud_service_name"],
					self.config["resource_type"],
					self.config["resource_name"]),
				"GET",
				None
			)
		
		if status in [200, 201]:
			Printer.info("Get resource succeeded. Checking response.")
		else:
			Printer.error("Get resource failed with HTTP status code %s" % status)
			return

		t = get_subtree_from_xml_string(response)
		self._validate_resource_response(etag, t)

	def get_cloud_service(self):
		Printer.start_test("Get CloudService")
		etag = generate_etag()

		(status, response) = self.client.perform_request(
				"subscriptions/%s/cloudservices/%s" % (
					self.config["subscription_id"],
					self.config["cloud_service_name"]
					),
				"GET",
				None
			)
		
		if status in [200, 201]:
			Printer.info("Get CloudService succeeded. Checking response.")
		else:
			Printer.error("Get CloudService failed with HTTP status code %s" % status)
			return

		t = get_subtree_from_xml_string(response)
		root_node_expected_tag = '{0}CloudService'.format(get_namespace(t))
		root_node_actual_tag = get_root_tag(t)
		if (root_node_expected_tag != root_node_actual_tag):
			Printer.error("Root node does not have expected tag %s" % root_node_expected_tag)
			return
		
		resources = get_nodes(t, ".//{0}Resource")
		for resource in resources:
			t = get_subtree_from_element(resource)
			self._validate_resource_response(etag, t)

	def upgrade(self):		
		etag = generate_etag()
		Printer.start_test("Update plan")

		# CHECK: Upgrade succeeds
		(status, response) = self.client.perform_request(
				"/subscriptions/%s/cloudservices/%s/resources/%s/%s" % (
					self.config["subscription_id"],
					self.config["cloud_service_name"],
					self.config["resource_type"],
					self.config["resource_name"]),
				'PUT',
				xml_for_create_resource(
					plan=self.config['upgrade_plan'],
					resource_type=self.config['resource_type'],
					promotion_code=self.config['promo_code'],
					etag=etag
				)
			)

		if status in [200, 201]:
			Printer.info("Upgrade Resource succeeded. Checking response.")
		else:
			Printer.error("Upgrade Resource failed with HTTP status code %s" % status)
			return

		t = get_subtree_from_xml_string(response)
		self._validate_resource_response(etag, t)

	def sso(self):
		(status, response) = self.client.perform_request(
				"subscriptions/%s/cloudservices/%s/resources/%s/%s/SsoToken" % (
						self.config["subscription_id"],
						self.config["cloud_service_name"],
						self.config["resource_type"],
						self.config["resource_name"]
					),
				"POST",
				None,
				uri_type="sso"
			)

		if status in [200, 201]:
			Printer.info("SSO token request succeeded. Checking response.")
		else:
			Printer.error("SSO token request failed with HTTP status code %s" % status)
			return

		t = get_subtree_from_xml_string(response)
		self._check_node_exists(t, "./{0}SsoToken/TimeStamp")
		self._check_node_exists(t, "./{0}SsoToken/Token")

		fragment = urllib.urlencode(
				{
					"token": get_node_value(t, "./{0}Token"),
					"timestamp": get_node_value(t, "./{0}TimeStamp")
				}
			)

		(status, response) = self.client.perform_request(
				"/sso?subid=%s&cloudservicename=%s&resourcetype=%s&resourcename=%s&%s" % (
			 		self.config["subscription_id"], 
			 		self.config["cloud_service_name"],
			  		self.config["resource_type"],
			 		self.config["resource_name"],
			 		fragment
					),
				"GET",
				None,
				uri_type="sso",
				validate_xml=False
			)

		if status in [200, 201]:
			Printer.info("SSO login succeeded.")
		else:
			Printer.error("SSO login request failed with HTTP status code %s" % status)
			return


	def create(self):
		etag = generate_etag()
		Printer.start_test("Create resource")
		(status, response) = self.client.perform_request(
				"/subscriptions/%s/Events" % self.config['subscription_id'],
				'POST',
				xml_for_subscription_event(
					self.config["subscription_id"], "Registered"
				)
			)

		# CHECK: Subscription Register event succeeds
		if status in [200, 201]:
			Printer.info("Subscription register event succeeded")
		else:
			Printer.error("Subscription register event failed with HTTP status code %s" % status)
			return
		
		# CHECK: Resource creation succeeds
		(status, response) = self.client.perform_request(
				"/subscriptions/%s/cloudservices/%s/resources/%s/%s" % (
					self.config["subscription_id"],			
					self.config["cloud_service_name"],
					self.config["resource_type"],
					self.config["resource_name"]),
				'PUT',
				xml_for_create_resource(
					plan=self.config['plan'],
					resource_type=self.config['resource_type'],
					promotion_code=self.config['promo_code'],
					etag=etag
				)
			)

		if status in [200,201]:
			Printer.info("Resource creation succeeded")
		else:
			Printer.error("Resource creation event failed with HTTP status code %s" % status)

		t = get_subtree_from_xml_string(response)
		self._validate_resource_response(etag, t)


	def delete(self):
		pass

	def manifest(self):
		pass

	def all(self):
		pass