import requests
import urlparse
import sys
import xmlutil
from utility import Printer, die

"""
Client is factored into its own class so we can swap out the HTTP request library in the future, if needed. For now,
we use Kenneth Reitz's excellent requests package
"""
class Client:
	def __init__(self, base_uri, sso_uri):
		self.base_uri = base_uri
		self.sso_uri = sso_uri
		self.headers =	{
							'accept':       'application/xml',
							'content-type': 'application/xml',
							'x-ms-version': '2012-03-01'
						}

	def perform_request(self, uri, method, body, uri_type='base', validate_xml=True, timeout=20.0):
		full_url = urlparse.urljoin(self.base_uri,uri) if uri_type == 'base' else urlparse.urljoin(self.sso_uri,uri)

		dispatch = { 
			'GET':		requests.get,
			'PUT': 		requests.put,
			'POST':		requests.post,
			'DELETE':	requests.delete
		}

		Printer.info("%s on %s" % (method, full_url))

		try:
			if method in ['PUT','POST']:
				result = dispatch[method](full_url, body, headers=self.headers)
			elif method in ['GET', 'DELETE']:
				result = dispatch[method](full_url, headers=self.headers)
		except requests.exceptions.ConnectionError as e:
			Printer.error("Could not %s on %s. Error: %s" % (method, full_url, e.message[1]))
			die()
		except requests.exceptions.Timeout as e:
			Printer.error("%s on %s timed out." % (method, full_url))
			die()

		Printer.info("Server returned HTTP status code %s" % result.status_code)

		if result.content and validate_xml:
			try:
				t = xmlutil.get_root_element(xmlutil.get_subtree_from_xml_string(result.content))
			except Exception as e:
				Printer.error("Could not parse response as XML. Check for mismatched tags or missing XML header. Error: %s" % e.message)
				die()

			try:
				xmlutil.check_tags_alpha_ordered(t)
			except xmlutil.TagOrderingException as e:
				Printer.error("Tags in response have to be alphabetically sorted. These tags are not alphabetically-sorted: %s" % e.message)
				die()

		return (result.status_code, result.content)
