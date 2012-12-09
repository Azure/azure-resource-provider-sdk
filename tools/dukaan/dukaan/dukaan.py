#!/usr/bin/env python
import os
import utility
import argparse
import xmlutil
import json
from clint import resources
from utility import Printer
from validator import Validator

config = {
	'manifest': None,
	'cloud_service_name': utility.random_cloud_service(),
	'promo_code': ""
}

def main():	
	# read config from per-user file
	read_config()

	# override config with optional arguments
	parse_arguments()

	if config['command'] == 'init':
		create_config()
	else:
		run_checks()

def create_config():
	resources.init("Microsoft", "Dukaan")
	resource_provider_namespace = raw_input("Resource Provider namespace [e.g. contoso]: ")
	resource_type = raw_input("Resource Type [e.g. monitoring]: ")
	subscription_id = raw_input("Subscription ID [e.g. my_subscription]: ")
	resource_name = raw_input("Resource Name [e.g. my_resource]: ")
	purchase_plan = raw_input("Base Plan Name [e.g. free]: ")
	upgrade_plan = raw_input("Upgrade Plan Name [e.g. gold]: ")

	config['resource_provider_namespace'] = resource_provider_namespace
	config['resource_type'] = resource_type
	config['subscription_id'] = subscription_id
	config['resource_name'] = resource_name
	config['purchase_plan'] = purchase_plan
	config['upgrade_plan'] = upgrade_plan

	resources.user.write('config.ini', json.dumps(config))

def read_config():
	resources.init("Microsoft", "Dukaan")
	contents = resources.user.read('config.ini')
	d = json.loads(contents)
	
	for k in d:
		config[k] = d[k]

def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("command", help="Command to run", choices=["init", "create", "show", "upgrade", "delete", "sso", "manifest"])
	parser.add_argument('--env', help='Environment to run tests in.', choices=['test', 'prod'], default='test')
	parser.add_argument('--manifest-path', help='Path to manifest.xml file. If not provided, dukaan will look in working directory for a file named manifest.xml')
	parser.add_argument("--resource-provider-namespace", help="Namespace of Resource Provider e.g. contoso")
	parser.add_argument("--subscription-id", help="Name of Subscription e.g. my_subscription")
	parser.add_argument("--cloud-service-name", help="Name of CloudService e.g. my_cloud_service")
	parser.add_argument("--resource-type", help="Type of Resource e.g. monitoring")
	parser.add_argument("--resource-name", help="Name of Resource e.g. myresource")
	parser.add_argument('--promo-code', help='Promotion code to use during Create Resource and Upgrade Resource')
	parser.add_argument('--plan', help='Plan name used during upgrades and purchases')
	
	parse_result = parser.parse_args()

	optionals = ['command', 'env', 'manifest_path', 'resource_provider_namespace', 'subscription_id', 'cloud_service_name', 'resource_type', 'resource_name', 'promo_code', 'plan']
	for optional in optionals:
		attribute_value = getattr(parse_result, optional)
		if attribute_value is not None:
			config[optional] = attribute_value	

def run_checks():
	if 'manifest_path' in config:
		manifest_path = config['manifest_path']
	else:
		manifest_path = os.path.join(os.getcwdu(), "manifest.xml")
		config['manifest_path'] = manifest_path

	try:
		with open(manifest_path) as f: pass
	except IOError as e:
		Printer.error("Manifest file %s could not be opened" % (manifest_path))
		utility.die()

	validator = Validator(config)
	dispatch = {
		'create':	validator.create,
		'show':		validator.get_cloud_service,
		'delete':	validator.delete,
		'upgrade':	validator.upgrade,
		'manifest':	validator.manifest,
		'sso':		validator.sso,
	}

	dispatch[config['command']]()

if __name__ == '__main__':
	main()