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
Adds trailing slash to URL. Needed for urlparse.urljoin to work per spec.
"""
def slashify(url):
	if (url[-1] == '/'):
		return url
	else:
		return url + '/'

"""
Removes trailing slash from URL. Needed for urlparse.urljoin to work per spec.
"""
def unslashify(url):
	if (url[-1] == '/'):
		return url[0:-1]
	else:
		return url

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
		return e.tag

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

def get_xmlns(t):	
	el = t.getroot()
	if el.tag[0] == "{":
		xmlns, _, _ = el.tag[1:].partition("}")
	else:
		xmlns = None
	return xmlns

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

def parse_manifest(manifest_path):
	with open(manifest_path) as f:
		manifest_content = f.read()
		errors = []
		warnings = []
		manifest_config = {'test': {}, 'prod': {}, 'output_items':[]}
		t = get_subtree_from_xml_string(manifest_content)

		test_base_uri_xpath = "./Test/ResourceProviderEndpoint"
		test_sso_uri_xpath = "./Test/ResourceProviderSsoEndpoint"
		prod_base_uri_xpath = "./Prod/ResourceProviderEndpoint"
		prod_sso_uri_xpath = "./Prod/ResourceProviderSsoEndpoint"

		if node_exists(t, test_base_uri_xpath):
			manifest_config['test']['base'] = slashify(get_node_value(t, test_base_uri_xpath))
			if not is_https(manifest_config['test']['base']):
				warnings.append("Base URI for Test environment is not HTTPS")

		else:
			errors.append("Base URI for Test environment is not defined in manifest.")

		if node_exists(t, test_sso_uri_xpath):
			manifest_config['test']['sso'] = unslashify(get_node_value(t, test_sso_uri_xpath))
			if not is_https(manifest_config['test']['sso']):
				warnings.append("SSO URI for Test environment is not HTTPS")
		else:
			errors.append("SSO URI for Test environment is not defined in manifest.")

		if node_exists(t, prod_base_uri_xpath):
			manifest_config['prod']['base'] = slashify(get_node_value(t, prod_base_uri_xpath))
			if not is_https(manifest_config['prod']['base']):
				warnings.append("Base URI for Prod environment is not HTTPS")
		else:
			errors.append("Base URI for Prod environment is not defined in manifest.")

		if node_exists(t, prod_sso_uri_xpath):
			manifest_config['prod']['sso'] = unslashify(get_node_value(t, prod_sso_uri_xpath))
			if not is_https(manifest_config['prod']['sso']):
				warnings.append("SSO URI for Prod environment is not HTTPS")
		else:
			errors.append("SSO URI for Prod environment is not defined in manifest.")

		output_items = get_nodes(t, ".//OutputItem/Name")
		if len(output_items) == 0:
			warnings.append("OutputItems are not defined in the manifest. If your Resource Provider exposes Output Items, please define them in the manifest.")
		else:
			manifest_config['output_items'] = [n.text for n in output_items]

		return errors, warnings, manifest_config

def xml_for_subscription_event(subscription_id, resource_provider, resource_type, event_type, etag=None):
	if not etag:
		etag = str(uuid.uuid1())

	template = """
<EntityEvent xmlns='http://schemas.datacontract.org/2004/07/Microsoft.Cis.DevExp.Services.Rdfe.ServiceManagement'>
	<EventId>%(subscription_id)s</EventId>
	<ListenerId>%(resource_provider)s</ListenerId>
	<EntityType>Subscription</EntityType>
	<EntityState>%(event_type)s</EntityState>
	<EntityId>
		<Id>%(subscription_id)s</Id>
		<Created>%(time_created)s</Created>
	</EntityId>
	<IsAsync>false</IsAsync>
	<OperationId>%(etag)s</OperationId>
	<Properties>
		<EntityProperty>
			<PropertyName>ResourceType</PropertyName>
			<PropertyValue>%(resource_type)s</PropertyValue>
		</EntityProperty>
		<EntityProperty>
			<PropertyName>EMail</PropertyName>
			<PropertyValue>someone@contoso.com</PropertyValue>
		</EntityProperty>
		<EntityProperty>
			<PropertyName>OptIn</PropertyName>
			<PropertyValue>false</PropertyValue>
		</EntityProperty>
	</Properties>
</EntityEvent>
	"""

	values = {
		'subscription_id': subscription_id,
		'resource_provider': resource_provider,
		'event_type': event_type,
		'time_created': str(datetime.now().isoformat()),
		'etag': etag,
		'resource_type': resource_type
	}
	return template % values

def xml_for_create_resource(plan, resource_type, region="West US", promotion_code="", etag=None):
	if not etag:
		etag = str(uuid.uuid1())


	template = """
<Resource xmlns='http://schemas.datacontract.org/2004/07/Microsoft.Cis.DevExp.Services.Rdfe.ServiceManagement'>
	<CloudServiceSettings>
		<GeoRegion>%(region)s</GeoRegion>
	</CloudServiceSettings>
	<ETag>%(etag)s</ETag>
	<IntrinsicSettings/>
	<PromotionCode>%(promotion_code)s</PromotionCode>
	<Plan>%(plan)s</Plan>
	<SchemaVersion>1.0</SchemaVersion>
	<Type>%(resource_type)s</Type>
	<Version>1.0</Version>
</Resource>
	"""

	values = {
		'region': region,
		'etag': etag,
		'promotion_code': promotion_code,
		'plan': plan,
		'resource_type': resource_type
	}

	return template % values
