#!/usr/bin/env python
import args
import os
import utility
import argparse
import string
import random
import uuid
import xmlutil
from utility import Printer
from validator import Validator

# default configuration
config = {
	'manifest_file': None,
	'operation': {},
	'manifest': None,
	'env': 'test',
	'cloud_service_name': 'test_cloud_service',
	'subscription_id': 'f6c18f8a-ab84-4e6d-b410-18710e8ef770',
	'resource_name': 'my_resource_instance',
	'promo_code': 'my_promo_code',
}

def main():
	parse_arguments()
	run_checks()

def random_cloud_service():
	random_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(52))
	result = "Azure-Stores-%s-Northwest-US" % random_string
	return result

def random_subscription():
	return str(uuid.uuid1())

def parse_arguments():
	parser = argparse.ArgumentParser()

	parser.add_argument('--env', help='Environment to run tests in.', choices=['test', 'prod'], default='test', required=False)
	parser.add_argument('--manifest', help='Path to manifest.xml file. If not provided, dukaan will look in working directory for a file named manifest.xml', type=argparse.FileType('r'))
	parser.add_argument('--promotion-code', help='Promotion code to use during Create Resource and Upgrade Resource', required=False)

	subparsers = parser.add_subparsers(title='subcommands', description='valid subcommands', help='additional help')

	# initialize config file
	parser_create = subparsers.add_parser('init')
	parser_create.add_argument('--config-file', help="Name of configuration file to write to", required=False, default=os.path.join(os.getcwdu(), "dukaan.config"))

	# test Create Resource
	parser_create = subparsers.add_parser('create')
	parser_create.add_argument('--resource-provider-namespace', help="Namespace of Resource Provider e.g. contoso", required=True)
	parser_create.add_argument('--subscription-name', help="Name of Subscription", default=random_subscription(), required=False)
	parser_create.add_argument('--cloud-service-name', help="Name of CloudService to create e.g. myresource", default=random_cloud_service(), required=False)
	parser_create.add_argument('--resource-type', help="ResourceType to create e.g. monitoring", required=True)
	parser_create.add_argument('--resource-name', help="Name of Resource to create e.g. myresource", default="myresource", required=False)
	parser_create.add_argument('--plan', help="Name of plan to create Resource with e.g. free", required=True)
	parser_create.set_defaults(which='create')

	# test Show Resource
	parser_create = subparsers.add_parser('show')
	parser_create.add_argument('--subscription-name', help="Name of Subscription", required=True)
	parser_create.add_argument('--cloud-service-name', help="Name of CloudService e.g. myresource", required=True)
	parser_create.add_argument('--resource-type', help="Type of Resource e.g. monitoring", required=True)
	parser_create.add_argument('--resource-name', help="Name of Resource to show e.g. myresource", required=True)
	parser_create.set_defaults(which='show')

	# test Upgrade Resource
	parser_create = subparsers.add_parser('upgrade')
	parser_create.add_argument('--subscription-name', help="Name of Subscription", required=True)
	parser_create.add_argument('--cloud-service-name', help="Name of CloudService e.g. myresource", required=True)
	parser_create.add_argument('--resource-type', help="Type of Resource e.g. monitoring", required=True)
	parser_create.add_argument('--resource-name', help="Name of Resource to upgrade e.g. myresource", required=True)
	parser_create.add_argument('--upgrade-plan', help="Identifier of plan to upgrade to e.g. gold", required=True)
	parser_create.set_defaults(which='upgrade')

	# test Delete Resource
	parser_create = subparsers.add_parser('delete')
	parser_create.add_argument('--subscription-name', help="Name of Subscription", required=True)
	parser_create.add_argument('--cloud-service-name', help="Name of CloudService e.g. myresource", required=True)
	parser_create.add_argument('--resource-type', help="Type of Resource e.g. monitoring", required=True)
	parser_create.add_argument('--resource-name', help="Name of Resource to delete e.g. myresource", required=True)
	parser_create.set_defaults(which='delete')

	# test SSO
	parser_create = subparsers.add_parser('sso')
	parser_create.add_argument('--subscription-name', help="Name of Subscription", required=True)
	parser_create.add_argument('--cloud-service-name', help="Name of CloudService e.g. myresource", required=True)
	parser_create.add_argument('--resource-type', help="Type of Resource e.g. monitoring", required=True)
	parser_create.add_argument('--resource-name', help="Name of Resource to SSO to e.g. myresource", required=True)
	parser_create.set_defaults(which='sso')
	
	parse_result = parser.parse_args()

	config['operation'] = parse_result.which
	config['manifest_file'] = parse_result.manifest if parse_result.manifest else config['manifest_file']
	config['subscription_id'] = parse_result.subscription_name if parse_result.subscription_name else config['subscription_name']
	config['cloud_service_name'] = parse_result.cloud_service_name if parse_result.cloud_service_name else config['cloud_service_name']
	config['resource_name'] = parse_result.resource_name if parse_result.resource_name else config['resource_name']
	config['resource_type'] = parse_result.resource_type

	if parse_result.promotion_code:
		config['promo_code'] = parse_result.promo_code
	if parse_result.which == "upgrade":
		config['upgrade_plan'] = parse_result.upgrade_plan
	if parse_result.which == "create":
		config['resource_provider_namespace'] = parse_result.resource_provider_namespace
		config['plan'] = parse_result.plan

	if config['manifest_file'] is None:
		default_manifest_path = os.path.join(os.getcwdu(), "manifest.xml")
		try:
			with open(default_manifest_path) as f: pass
		except IOError as e:
			Printer.error("manifest.xml not found in working directory %s. Use the --manifest switch to specify the absolute path to the manifest." % default_manifest_path)
			utility.die()

	errors, warnings, manifest_config = xmlutil.parse_manifest(config['manifest_file'])
	if errors or warnings:
		Printer.start_test('Checking manifest')
	for error in errors:
		Printer.error("Manifest: %s" % error)

	for warning in warnings:
		Printer.warn("Manifest: %s" % warning)

	config['manifest'] = manifest_config

def run_checks():
	validator = Validator(config)
	dispatch = {
		'create':	validator.create,
		'show':		validator.get_cloud_service,
		'delete':	validator.delete,
		'upgrade':	validator.upgrade,
		'manifest':	validator.manifest,
		'sso':		validator.sso,
	}

	dispatch[config['operation']]()

if __name__ == '__main__':
	main()