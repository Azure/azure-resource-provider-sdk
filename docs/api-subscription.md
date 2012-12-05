Subscription API
===
When a user purchases your offering, Windows Azure will start sending your RP *subscription lifecycle events* about the subscription the resource was created in. For example, if a user purchases Clouditrace on the "3-month Free Trial" subscription, the Clouditrace RP will start receiving subscription lifecycle events about this particular subscription. For example, if the user fails to pay their bill, your RP will be notified so your service can take appropriate action.

**It is important that you response appropriately to each subscription lifecycle event to prevent your service from going out of sync with Windows Azure**


Request
--
URL: `https://<base_uri>/subscriptions/<subscription_id>/Events`

Method: `POST`

Sample:

```xml
<?xml version="1.0" encoding="utf-8"?>
<EntityEvent>
	<EventId>766ed3be-11be-4a88-a7c8-ba4286299066</EventId>
	<EntityType>Subscription</EntityType>
	<EntityState>Registered</EntityState>
	<EntityId>
		<Id>f6c18f8a-ab84-4e6d-b410-18710e8ef770</Id>
		<Created>2012-10-12T06:42:36.8265209Z</Created>
	</EntityId>
	<OperationId>ae9a07ef-2306-40e0-bbe5-2821352a8c4d</OperationId>
	<Properties>
		<EntityProperty>
			<PropertyName>ResourceType</PropertyName>
			<PropertyValue>monitoring</PropertyValue>
		</EntityProperty>
		<EntityProperty>
			<PropertyName>EMail</PropertyName>
			<PropertyValue>someone@contoso.com</PropertyValue>
		</EntityProperty>
		<EntityProperty>
			<PropertyName>OptIn</PropertyName>
			<PropertyValue>True</PropertyValue>
		</EntityProperty>
	</Properties>
</EntityEvent>
```

* `EventId` is the ID of the subscription. **This field is deprecated and should not be used**.
* `EntityType` will always be _Subscription_. **This field can be ignored**.
* `EntityId/Id` is the ID of the subscription. It is a GUID, and should be stored by your service. Note that this is the Subscription ID and should be recorded by your service.
* `EntityId/EntityEvent` is the actual event. It can take four values: `Registered`, `Disabled`, `Enabled`, `Deleted`.
  * `Registered` This tells the RP that the user intends to create a resource under this subscription.
  * `Disabled` The user's Windows Azure subscription has been disabled, due to fraud or non-payment. Your RP should make the resource inaccessible without deleting its data.
  * `Enabled` The user's Windows Azure subscription has been enabled, because it is current on payments. Your RP should restore access to data.
  * `Deleted` The user's Windows Azure subscription has been deleted. Windows Azure retains data for 90 days. We recommend a similar retention policy.
* `OperationId` is a unique identifier for this subscription lifecycle event. It is similar in spirit to the ETag, because a subscription lifecycle event that is not acknowledged with an HTTP status code `200` or `201` will be retried again with the same `OperationId`.
* `Properties` is a property bag that Windows Azure passes to the RP. Only two properties are supported today:
  * `EMail` is the e-mail address of the logged-in user.
  * `OptIn` indicates whether the user has agreed to give you additional permissions about sending them marketing material. Your RP can always send transactional e-mails e.g. about service or account issues to the e-mail address given in the `EMail` field.

Response
---
If the event is processed successfully, your RP should return a `200` or `201` HTTP status code.