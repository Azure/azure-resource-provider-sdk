from xmlbuilder import XMLBuilder
from datetime import datetime
import uuid
import utility

def xml_for_subscription_event(subscription_id, event_type, resource_provider_namespace="cloudkeys", etag=None):
	if not etag:
		etag = utility.generate_etag()

	headers = [('Content-Type', 'application/xml')]
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

def xml_for_create_resource(region="West US", promotion_code=None, intrinsic_settings=None, etag=None, plan="Free"):
	if not etag:
		etag = str(uuid.uuid1())

	headers = [('Content-Type', 'application/xml')]
	x = XMLBuilder('Resource', xmlns='http://schemas.microsoft.com/windowsazure')
	with x.CloudServiceSettings:
		x.GeoRegion(region)
	x.ETag(etag)
	x.IntrinsicSettings(intrinsic_settings)
	x.PromotionCode(promotion_code)
	x.Plan(plan)
	x.SchemaVersion("1.0")
	x.Type("cloudkeys")
	x.Version("1.0")
	return str(x)