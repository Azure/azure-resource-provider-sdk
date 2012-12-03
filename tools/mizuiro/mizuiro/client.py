import requests
import urlparse
from utility import Printer
from xml.dom import minidom

class TagOrderingException(Exception):
	pass

class Client:
	def __init__(self, base_uri, sso_uri):
		self.base_uri = base_uri
		self.sso_uri = sso_uri
		self.headers =	{
							'content-type': 'application/xml',
							'x-ms-version': '2012-03-01'
						}

	# CHECK: Validate tag alpha ordering
	def validate_tag_alpha_ordering(self, t):
		# minidom makes me recurse to get siblings - should fix the perf here
		def getSiblings(t, l):
			if t.nextSibling:
				if t.nextSibling.nodeType == t.ELEMENT_NODE:
					l.append(t)
				getSiblings(t.nextSibling,l)
			return l

		elem_children = [c for c in t.childNodes if c.nodeType == c.ELEMENT_NODE]

		# get rid of whitespace children
		whitespace_children =  [c for c in t.childNodes if c.nodeType == c.TEXT_NODE and c.nodeValue.isspace()]
		for child in whitespace_children:
			t.removeChild(child)

		if t.nodeType == t.ELEMENT_NODE:			
			siblings = getSiblings(t,[])
			sibling_tag_names = [n.nodeName for n in siblings]
					
			if sibling_tag_names != sorted(sibling_tag_names):
				raise TagOrderingException()

		for child in elem_children:
			self.validate_tag_alpha_ordering(child)

		return

	def perform_request(self, uri, method, body, uri_type='base', validate_xml=True):
		if uri_type=='base':
			full_url = urlparse.urljoin(self.base_uri,uri)
		else:
			full_url = urlparse.urljoin(self.sso_uri,uri)
		dispatch = { 
			'GET':		requests.get,
			'PUT': 		requests.put,
			'POST':		requests.post,
			'DELETE':	requests.delete
		}

		if method in ['PUT','POST','DELETE']:
			result = dispatch[method](full_url, body, headers=self.headers)
		else:
			result = dispatch[method](full_url, headers=self.headers)

		if result.content and validate_xml:
			try:
				t = minidom.parseString(result.content)
			except:
				Printer.error("Could not parse response as XML. Check for mismatched tags or missing XML header.")
				return (None, None)

			try:
				self.validate_tag_alpha_ordering(t)
			except TagOrderingException:
				Printer.error("Tags in response have to be alphabetically sorted. These tags are not alpha-sorted: %s" % siblings.join(', '))

			if not t.encoding:
				Printer.error("Response requires a valid header such as <?xml version='1.0' encoding='utf-8'?>")

		return (result.status_code, result.content)