from xmlbuilder import XMLBuilder
from datetime import datetime
from xml.etree.ElementTree import ElementTree, XML, fromstring, Element

import uuid
import re

class RootNodeNotFoundException(Exception): pass
class NodeNotFoundException(Exception): pass
class NodeValueMismatchException(Exception): pass
class NamespaceMissingException(Exception): pass


"""
Gets an ElementTree subtree from the first node matching the XPath
"""
def get_subtree(t, xpath):
	root = t.find(xpath.format(get_namespace(t)))
	if not root:
		raise NodeNotFoundException("Node matching xpath %s was not found in tree with root node <%s>" % root.tag)
	return ElementTree(t)

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
	match = t.find(xpath.format(get_namespace(t)))
	return match is not None

def get_root_tag(t):
	root = t.getroot()
	if root is None:
		raise RootNodeNotFoundException()
	return root.tag

def get_node_value(t, xpath):
	if not node_exists(t, xpath):
		raise NodeNotFoundException

	return t.find(xpath.format(get_namespace(t))).text

def get_nodes(t, xpath):
	return t.findall(xpath.format(get_namespace(t)))

def xml_for_subscription_event(subscription_id, event_type, resource_provider_namespace="cloudkeys", etag=None):
	if not etag:
		etag = str(uuid.uuid1())

	x = XMLBuilder('EntityEvent', xmlns='http://schemas.microsoft.com/windowsazure')
	x.EventId(subscription_id)
	x.ListenerId(resource_provider_namespace)
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
			x.PropertyValue("cloudkeys")
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