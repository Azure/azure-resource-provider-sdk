import untangle
import os
from clint.textui import colored
import sys
import uuid

def generate_etag():
	return str(uuid.uuid1())

def parse_manifest(path):
	manifest_config = {'test': {}, 'prod': {}, 'output_keys':[]}
	manifest_content = open(path, 'r').read()
	obj = untangle.parse(manifest_content)
	try:
		test = obj.ResourceManifest.Test
		try:
			manifest_config['test']['base'] = obj.ResourceManifest.Test.ResourceProviderEndpoint.cdata
			manifest_config['test']['sso'] = obj.ResourceManifest.Test.ResourceProviderSsoEndpoint.cdata
		except IndexError:
			Printer.error("<Test> has missing or malformed <ResourceProviderEndpoint> or <ResourceProviderSsoEndpoint> child nodes.")
	except IndexError:
		Printer.error("Test configuration is missing in manifest %s. Testing will stop." % path)
		sys.exit(0)

	try:
		test = obj.ResourceManifest.Prod
		try:
			manifest_config['prod']['base'] = obj.ResourceManifest.Prod.ResourceProviderEndpoint.cdata
			manifest_config['prod']['sso'] = obj.ResourceManifest.Prod.ResourceProviderSsoEndpoint.cdata
		except IndexError:
			Printer.error("<Prod> has missing or malformed <ResourceProviderEndpoint> or <ResourceProviderSsoEndpoint> child nodes.")
	except IndexError:
		Printer.warn("Prod configuration is missing in manifest %s." % path)
		sys.exit(0)

	try:
		output_keys = obj.ResourceManifest.OutputKeys
		for child in output_keys.children:
			manifest_config['output_keys'].append(child.Name.cdata)

	except IndexError:
		Printer.warn("<OutputKeys> not found. Make sure your Resource Provider does not expose Output Keys.")

	return manifest_config

class Printer:
	@staticmethod
	def start_test(message):
		print(
"""
=========================
Starting test %s
=========================
""" % message
			)

	@staticmethod
	def warn(message):
		print colored.yellow("[WARN] %s" % message)

	@staticmethod
	def error(message):
		print colored.red("[FAIL] %s" % message)

	@staticmethod
	def info(message):
		print colored.green("[PASS] %s" % message)