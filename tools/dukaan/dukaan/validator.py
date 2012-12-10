import re
import string
import urllib
import iso8601
import xmlutil
from datetime import datetime, timedelta
from client import Client
from utility import Printer, generate_etag

class Validator(object):
	def __init__(self,config):
		self.config = config
		errors, warnings, manifest_config = xmlutil.parse_manifest(self.config['manifest_path'])
		config['manifest'] = manifest_config
		env = self.config['env']		

		self.client = Client(
			config['manifest'][env]['base'],
			config['manifest'][env]['sso']
			)

	def _check_node_exists(self, t, xpath, behavior="error"):
		try:
			xmlutil.node_exists(t, xpath)
		except NodeNotFoundException:
			msg = "XPath %s was not found in the response" % xpath
			if behavior == "error":
				Printer.error(msg)
			else:
				Printer.warn(msg)

	def _check_node_value(self, t, xpath, expected):
		try:
			actual = xmlutil.get_node_value(t, xpath)
			if actual != expected:
				Printer.error("Node at XPath %s has actual value %s, expected value %s" % (xpath, actual, expected))

		except NodeNotFoundException:
			Printer.error("Node at XPath %s was not found in the response" % xpath)

	def _validate_resource_response(self, etag, t):
		root_node_expected_tag = xmlutil.get_root_tag(t)
		Printer.info("Checking if root node's tag is %s" % root_node_expected_tag)
		root_node_actual_tag = xmlutil.get_root_tag(t)

		if (root_node_expected_tag != root_node_actual_tag):
			Printer.error("Root node does not have expected tag %s" % root_node_expected_tag)

		Printer.info("Checking if CloudServiceSettings are present")
		self._check_node_exists(t, './{0}CloudServiceSettings')
		
		if etag:
			Printer.info("Checking if ETag is %s" % etag)
			self._check_node_value(t, './{0}ETag', etag)
		Printer.info("Checking if Name is %s" % self.config['resource_name'])
		self._check_node_value(t, './{0}Name', self.config['resource_name'])
	
		Printer.info("Checking if OperationStatus/Result is 'Succeeded'")
		self._check_node_value(t, './{0}OperationStatus/{0}Result', "Succeeded")
		
		Printer.info("Checking if OutputItems are present")
		if self._check_node_exists(t, './{0}OutputItems', behavior='warn'):
			output_items = t.findall('.//{0}OutputItem'.format(xmlutil.get_namespace(t)))
			for output_item in output_items:
				output_item_tree = xmlutil.get_subtree_from_element(output_item)
				self._check_node_exists(output_item_tree, './{0}Key')
				self._check_node_exists(output_item_tree, './{0}Value')

		Printer.info("Checking if UsageMeters are present")
		if self._check_node_exists(t, './{0}UsageMeters', behavior='warn'):
			usage_meters = xmlutil.get_nodes('.//{0}UsageMeter')
			for usage_meter in usage_meters:
				usage_meter_tree = xmlutil.get_subtree_from_element(usage_meter)
				self._check_node_exists(usage_meter_tree, './{0}Included')
				self._check_node_exists(usage_meter_tree, './{0}Name')
				self._check_node_exists(usage_meter_tree, './{0}Unit', behavior='warn')
				self._check_node_exists(usage_meter_tree, './{0}Used')

		Printer.info("Checking if Plan is present")
		self._check_node_exists(t, './{0}Plan')

		Printer.info("Checking if State is 'Started'")
		self._check_node_value(t, './{0}State', "Started")

	def get_resource(self):
		Printer.start_test("Get Resource")

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
			Printer.success("Get resource succeeded.")
			Printer.info("Checking XML")
		else:
			Printer.error("Get resource failed with HTTP status code %s" % status)
			return

		t = xmlutil.get_subtree_from_xml_string(response)
		self._validate_resource_response(None, t)

	def get_cloud_service(self):
		Printer.start_test("Get CloudService")

		(status, response) = self.client.perform_request(
				"subscriptions/%s/cloudservices/%s" % (
					self.config["subscription_id"],
					self.config["cloud_service_name"]
					),
				"GET",
				None
			)
		
		if status in [200, 201]:
			Printer.success("Get CloudService succeeded.")
			Printer.info("Checking XML")
		else:
			Printer.error("Get CloudService failed with HTTP status code %s" % status)
			return

		t = xmlutil.get_subtree_from_xml_string(response)
		root_node_expected_tag = '{0}CloudService'.format(xmlutil.get_namespace(t))
		root_node_actual_tag = xmlutil.get_root_tag(t)
		if (root_node_expected_tag != root_node_actual_tag):
			Printer.error("Root node does not have expected tag %s" % root_node_expected_tag)
			return

		resource_names = map(lambda t: t.text, xmlutil.get_nodes(t, ".//{0}Resource/{0}Name"))
		
		if self.config['resource_name'] not in resource_names:
			Printer.error("Resource named '%s' not returned by endpoint" % self.config['resource_name'])

	def upgrade(self):		
		etag = generate_etag()
		Printer.start_test("Update plan")

		# CHECK: Plan upgrade succeeds
		(status, response) = self.client.perform_request(
				"/subscriptions/%s/cloudservices/%s/resources/%s/%s" % (
					self.config["subscription_id"],
					self.config["cloud_service_name"],
					self.config["resource_type"],
					self.config["resource_name"]),
				'PUT',
				xmlutil.xml_for_create_resource(
					plan=self.config['upgrade_plan'],
					resource_type=self.config['resource_type'],
					promotion_code=self.config['promo_code'],
					etag=etag
				)
			)

		if status in [200, 201]:
			Printer.success("Upgrade Resource succeeded.")
			Printer.info("Checking XML")
		else:
			Printer.error("Upgrade Resource failed with HTTP status code %s" % status)
			return

		t = xmlutil.get_subtree_from_xml_string(response)
		self._validate_resource_response(etag, t)
		Printer.info("Checking if new plan is %s" % self.config['upgrade_plan'])
		self._check_node_value(t, './{0}Plan', self.config['upgrade_plan'])

	def sso(self):
		Printer.start_test("SSO with valid timestamp and token")
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
			Printer.success("SSO token request succeeded.")
			Printer.info("Checking XML")
		else:
			Printer.error("SSO token request failed with HTTP status code %s" % status)
			return

		t = xmlutil.get_subtree_from_xml_string(response)
		self._check_node_exists(t, "./{0}SsoToken/TimeStamp")
		self._check_node_exists(t, "./{0}SsoToken/Token")

		fragment = urllib.urlencode(
				{
					"token": xmlutil.get_node_value(t, "./{0}Token"),
					"timestamp": xmlutil.get_node_value(t, "./{0}TimeStamp")
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
			Printer.success("SSO login succeeded.")
		else:
			Printer.error("SSO login request failed with HTTP status code %s" % status)
			return


		Printer.start_test("SSO with expired timestamp")
		given_timestamp = iso8601.parse_date(xmlutil.get_node_value(t, "./{0}TimeStamp"))
		expired_timestamp = given_timestamp + timedelta(seconds=60*10)
		
		fragment = urllib.urlencode(
				{
					"token": xmlutil.get_node_value(t, "./{0}Token"),
					"timestamp": str(expired_timestamp)
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
			Printer.error("SSO login with expired timestamp succeeded.")
		else:
			Printer.success("SSO login with expired timestamp failed with error code %s" % status)
			return


	def create(self):
		etag = generate_etag()
		Printer.start_test("Create resource")
		(status, response) = self.client.perform_request(
				"/subscriptions/%s/Events" % self.config['subscription_id'],
				'POST',
				xmlutil.xml_for_subscription_event(
					self.config["subscription_id"],
					self.config["resource_provider_namespace"],
					self.config["resource_type"],
					"Registered"
				)
			)

		# CHECK: Subscription Register event succeeds
		if status in [200, 201]:
			Printer.success("Subscription register event succeeded")
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
				xmlutil.xml_for_create_resource(
					plan=self.config['purchase_plan'],
					resource_type=self.config['resource_type'],
					promotion_code=self.config['promo_code'],
					etag=etag
				)
			)

		if status in [200,201]:
			Printer.success("Resource creation succeeded")
			Printer.info("Checking XML")
		else:
			Printer.error("Resource creation event failed with HTTP status code %s" % status)

		t = xmlutil.get_subtree_from_xml_string(response)
		self._validate_resource_response(etag, t)

	def delete(self):
		etag = generate_etag()
		Printer.start_test("Delete Resource")

		(status, response) = self.client.perform_request(
				"/subscriptions/%s/cloudservices/%s/resources/%s/%s" % (
					self.config["subscription_id"],
					self.config["cloud_service_name"],
					self.config["resource_type"],
					self.config["resource_name"]),
				'DELETE',
				None
			)

		if status in [200, 201]:
			Printer.success("Delete Resource succeeded.")
		else:
			Printer.error("Delete Resource failed with HTTP status code %s" % status)
			return

	def manifest(self):
		errors, warnings, manifest_config = xmlutil.parse_manifest(self.config['manifest_path'])
		if errors or warnings:
			Printer.start_test('Checking manifest')
		for error in errors:
			Printer.error("Manifest: %s" % error)

		for warning in warnings:
			Printer.warn("Manifest: %s" % warning)