#!/usr/bin/env python
import os
import utility
import argparse
import xmlutil
import json
import string
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
		validate_config()
		run_checks()

"""
Check if the config dictionary contains all the valid inputs needed to run a command
"""
def validate_config():
	required = {
		'create': ['resource_provider_namespace', 'resource_type', 'subscription_id', 'resource_name', 'purchase_plan'],
		'show':	['resource_provider_namespace', 'resource_type', 'subscription_id', 'resource_name'],
		'delete': ['resource_provider_namespace', 'resource_type', 'subscription_id', 'resource_name'],
		'upgrade': ['resource_provider_namespace', 'resource_type', 'subscription_id', 'resource_name', 'upgrade_plan'],
		'sso': ['resource_provider_namespace', 'resource_type', 'subscription_id', 'resource_name'],
		'manifest': []
	}

	missing = map(
					lambda x: x.replace("_", "-"),
					["--" + k for k in required[config['command']] if k not in config]
		)
	if missing:
		Printer.error("The following flags are required for this command: %s" % string.join(missing, ', '))
		utility.die()

"""
Prompts user for config values and Writes them to a per-user configuration file.
On Mac OS X, this is in /Users/JohnDoe/Library/Application Support/Dukaan/config.ini
"""
def create_config():
	def IsNotEmpty(s):
		return s != ""

	resources.init("Microsoft", "Dukaan")
	resource_provider_namespace = utility.get_input("Resource Provider namespace [e.g. contoso]: ", IsNotEmpty)
	resource_type = utility.get_input("Resource Type [e.g. monitoring]: ", IsNotEmpty)
	subscription_id = utility.get_input("Subscription ID [e.g. my_subscription]: ", IsNotEmpty)
	resource_name = utility.get_input("Resource Name [e.g. my_resource]: ", IsNotEmpty)
	purchase_plan = utility.get_input("Base Plan Name [e.g. free]: ", IsNotEmpty)
	upgrade_plan = utility.get_input("Upgrade Plan Name [e.g. gold]: ", IsNotEmpty)

	config['resource_provider_namespace'] = resource_provider_namespace
	config['resource_type'] = resource_type
	config['subscription_id'] = subscription_id
	config['resource_name'] = resource_name
	config['purchase_plan'] = purchase_plan
	config['upgrade_plan'] = upgrade_plan

	resources.user.write('config.ini', json.dumps(config))

"""
Returns configuration values from per-user configuration file
"""
def read_config():
	resources.init("Microsoft", "Dukaan")
	contents = resources.user.read('config.ini')
	if contents:
		d = json.loads(contents)	
		for k in d:
			config[k] = d[k]
	else:
		Printer.info("Configuration is empty. Run 'dukaan init' to save common settings to configuration file.")

"""
Parse optional arguments from command line. Optional arguments override values in the per-user configuration file.
"""
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