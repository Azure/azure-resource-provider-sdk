#!/usr/bin/env python
import args
import os
import utility
from validator import Validator

# default configuration
config = {
	'manifest_path': os.path.join(os.getcwdu(), "manifest.xml"),
	'operation': {},
	'manifest': None,
	'env': 'test',
	'cloud_service_name': 'test_cloud_service',
	'subscription_id': 'f6c18f8a-ab84-4e6d-b410-18710e8ef770',
	'resource_type': 'my_resource',
	'resource_name': 'my_resource_instance',
	'promo_code': 'my_promo_code',
	'plan': 'my_plan',
	'upgrade_plan': 'my_better_plan'
}

def main():
	parse_arguments()
	dispatch()

def parse_arguments():
	# operation
	if '--operation' in args.flags:
		config['operation']['name'] = args.grouped['--operation'].pop(0)
		config['operation']['flags'] = []
		flag = args.grouped['--operation'].pop(0)
		while flag:
			config['operation']['flags'].append(flag)
			flag = args.grouped['--operation'].pop(0)
	else:
		help("--operation flag must be specified e.g. --operation check")

	# environment
	if '--env' in args.flags:
		config['env'] = args.grouped['--env'].get(0)

	# manifest
	if '--manifest-path' in args.flags:
		manifest_path = args.grouped['--manifest-path'].get(0)
		try:
			with open(manifest_path) as f: pass
			config['manifest_path'] = manifest_path
		except IOError as e:
			help("Manifest file %s not found" % manifest_path)

	config['manifest'] = utility.parse_manifest(config['manifest_path'])

def dispatch():
	if config['operation']['name'] == 'check':
		run_check()
	else:
		help()

def help(message):
	base = """
	Usage: mizuiro.py <operation> <arguments>

	e.g.

	mizuiro.py --operation check create
	mizuiro.py --operation check create --manifest-path /rp/manifest.xml
	mizuiro.py --operation check create --env test --manifest-path /rp/manifest.xml

	"""
	print message + "\n" + base

def run_check():
	validator = Validator(config)
	dispatch = {
		'create':	validator.create,
		'get':		validator.get_cloud_service,
		'delete':	validator.delete,
		'upgrade':	validator.upgrade,
		'manifest':	validator.manifest,
		'sso':		validator.sso,
	}

	if config['operation']['flags']:
		choice = config['operation']['flags'][0]
	else:
		choice = 'all'

	if choice == 'all':
		for check in dispatch:
			dispatch[check]()
	else:
		dispatch[choice]()

if __name__ == '__main__':
	main()