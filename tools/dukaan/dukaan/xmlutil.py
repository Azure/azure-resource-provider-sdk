from xmlbuilder import XMLBuilder
from datetime import datetime
from xml.etree.ElementTree import ElementTree, XML, fromstring, Element
from urlparse import urlparse
import uuid
import re

class RootNodeNotFoundException(Exception): pass
class NodeNotFoundException(Exception): pass
class NodeValueMismatchException(Exception): pass
class NamespaceMissingException(Exception): pass
class TagOrderingException(Exception): pass

def is_https(url):
	return (urlparse(url)).scheme == 'https'

"""
Gets an ElementTree subtree from the first node matching the XPath
"""
def get_subtree(t, xpath):
	root = t.find(xpath.format(get_namespace(t)))
	if not root:
		raise NodeNotFoundException("Node matching xpath %s was not found in tree with root node <%s>" % root.tag)
	return ElementTree(t)

def normalized_xpath(t, xpath):
	regex = re.compile("{(.*)}(.*)")
	matches = regex.findall(xpath)
	if matches:
		return xpath.format(get_namespace(t))
	return xpath

def pretty_tag(e):
	regex = re.compile("{(.*)}(.*)")
	matches = regex.findall(e.tag)
	if matches:
		return matches[0][1]
	else:
		return e.etag

def get_subtree_from_element(e):	
	return ElementTree(e)

def get_subtree_from_xml_string(xml_string):
	return ElementTree(fromstring(xml_string))

def get_namespace(t):
	regex = re.compile("{(.*)}(.*)")
	matches = regex.findall(t.getroot().tag)
	if matches:
		return ("{" + matches[0][0] + "}")
	else:
		raise NamespaceMissingException()

def node_exists(t, xpath):
	match = t.find(normalized_xpath(t,xpath))
	return match is not None

def get_root_tag(t):
	root = t.getroot()
	if root is None:
		raise RootNodeNotFoundException()
	return root.tag

def get_root_element(t):
	root = t.getroot()
	if root is None:
		raise RootNodeNotFoundException()
	return root	

def get_node_value(t, xpath):
	if not node_exists(t, xpath):
		raise NodeNotFoundException

	return t.find(normalized_xpath(t,xpath)).text

def get_nodes(t, xpath):
	return t.findall(normalized_xpath(t, xpath))

def check_tags_alpha_ordered(e):
	children = e.getchildren()
	child_tags = [pretty_tag(child) for child in children]
	if child_tags != sorted(child_tags):
		raise TagOrderingException(', '.join(child_tags))

	for child in children:
		check_tags_alpha_ordered(child)

def parse_manifest(f):
	errors = []
	warnings = []
	manifest_config = {'test': {}, 'prod': {}, 'output_keys':[]}
	manifest_content = f.read()
	t = get_subtree_from_xml_string(manifest_content)

	test_base_uri_xpath = "./Test/ResourceProviderEndpoint"
	test_sso_uri_xpath = "./Test/ResourceProviderSsoEndpoint"
	prod_base_uri_xpath = "./Prod/ResourceProviderEndpoint"
	prod_sso_uri_xpath = "./Prod/ResourceProviderSsoEndpoint"

	if node_exists(t, test_base_uri_xpath):
		manifest_config['test']['base'] = get_node_value(t, test_base_uri_xpath)
		if not is_https(manifest_config['test']['base']):
			warnings.append("Base URI for Test environment is not HTTPS")

	else:
		errors.append("Base URI for Test environment is not defined in manifest.")

	if node_exists(t, test_sso_uri_xpath):
		manifest_config['test']['sso'] = get_node_value(t, test_sso_uri_xpath)
		if not is_https(manifest_config['test']['sso']):
			warnings.append("SSO URI for Test environment is not HTTPS")
	else:
		errors.append("SSO URI for Test environment is not defined in manifest.")

	if node_exists(t, prod_base_uri_xpath):
		manifest_config['prod']['base'] = get_node_value(t, prod_base_uri_xpath)
		if not is_https(manifest_config['prod']['base']):
			warnings.append("Base URI for Prod environment is not HTTPS")
	else:
		errors.append("Base URI for Prod environment is not defined in manifest.")

	if node_exists(t, prod_sso_uri_xpath):
		manifest_config['prod']['sso'] = get_node_value(t, prod_sso_uri_xpath)
		if not is_https(manifest_config['prod']['sso']):
			warnings.append("SSO URI for Prod environment is not HTTPS")
	else:
		errors.append("SSO URI for Prod environment is not defined in manifest.")

	output_keys = get_nodes(t, ".//OutputKey/Name")
	if len(output_keys) == 0:
		warnings.append("OutputKeys are not defined in the manifest. If your Resource Provider exposes Output Items, please define them in the manifest.")

	return errors, warnings, manifest_config

def xml_for_subscription_event(subscription_id, resource_provider, resource_type, event_type, etag=None):
	if not etag:
		etag = str(uuid.uuid1())

	x = XMLBuilder('EntityEvent', xmlns='http://schemas.microsoft.com/windowsazure')
	x.EventId(subscription_id)
	x.ListenerId(resource_provider)
	x.EntityType("Subscription")
	x.EntityState(event_type)
	with x.EntityId:
		x.Id(subscription_id)
		x.Created(str(datetime.now()))
	x.IsAsync("false")
	x.OperationId(etag)
	with x.Properties:
		with x.EntityProperty:
			x.PropertyName("ResourceType")
			x.PropertyValue(resource_type)
		with x.EntityProperty:
			x.PropertyName("EMail")
			x.PropertyValue("someone@foo.com")		
		with x.EntityProperty:
			x.PropertyName("OptIn")
			x.PropertyValue("False")	

	return str(x)

def xml_for_create_resource(plan, resource_type, region="West US", promotion_code="", etag=None):
	if not etag:
		etag = str(uuid.uuid1())

	x = XMLBuilder('Resource', xmlns='http://schemas.microsoft.com/windowsazure')
	with x.CloudServiceSettings:
		x.GeoRegion(region)
	x.ETag(etag)
	x.IntrinsicSettings()
	x.PromotionCode(promotion_code)
	x.Plan(plan)
	x.SchemaVersion("1.0")
	x.Type(resource_type)
	x.Version("1.0")
	return str(x)