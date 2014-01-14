# Resource Provider API Guide

A _Resource Provider_ (RP) is a web service that allows users to purchase an Add-on from the Windows Azure Store and manage it from within the Windows Azure Management Portal.  Each Add-on in the Windows Azure Store has it's own Resource Provider that communicates with the Windows Azure platform, in order to support the various workflows involved in supporting an Add-on in the Store.

***Please Note:*** the Windows Azure Store is currently in Preview and we are actively improving the Resource Provider API based on feedback. Please make sure you read these  [important tips and gotchas](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/tips-and-tricks.md) before you start implementing your own RP.

Read [Concepts](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/concepts.md) to understand the definitions and concept mappings for the Windows Azure platform and Resource Provider API.

##Resource Provider API Documentation

The Resource Provider (RP) API is:

- HTTP RESTful, using verbs like GET, PUT, DELETE to manage resources
- XML-based. There is no support for JSON yet.
- Authentication is through X.509 certificates.

###Handling Requests
You should expect requests on two endpoints defined in the Publisher Portal. You will receive resource lifecycle requests such as create, delete, update etc. on the *base URL* `https://<base_uri>/azurestore`. Single sign-on requests will come on the *SSO URL* `https://<base_uri>/azurestore/sso`.

Requests will be made in XML. JSON is not currently supported, but is being considered for future versions of the API.

You should expect two headers. The `content-type` header will be set to `application/xml`. The `x-ms-version` header will be set to `2012-03-01` or later.

[ETags](http://en.wikipedia.org/wiki/HTTP_ETag) in request and response bodies allow Windows Azure to cache your results. Windows Azure ETags are [GUIDs](http://en.wikipedia.org/wiki/Globally_unique_identifier). You are expected to keep track of ETags since Windows Azure will retry failed operations with the same ETag.

###Making Responses
Your RP should respond in less than 20 seconds to requests, otherwise Windows Azure will consider the operation timed out.

Responses adhere to standard HTTP conventions. For simplicity, HTTP codes `200` and `201` are considered equivalent. `403` is used to indicated unauthorized access. `409`, codes in the `5xx` range and timeouts are considered errors, and Windows Azure will retry with the same ETag.

Where a response body is required, you are expected to return XML. JSON is not currently supported, but is being considered for future versions of the API.

Make sure to set the `content-type` header to `application/xml`.

If your response size is greater than 1 MB, you will receive an HTTP code `500`.

Generally, case matters everywhere e.g. `started != Started`

###Authentication
The RP API is one-way, i.e. Windows Azure can call your service, but your service cannot call Windows Azure. All calls are made over HTTPS.

You are responsible for verifying the caller's certificate thumbprint. **Only accept calls from certificates that have the correct public key**.

Below are the certificates used by Windows Azure to call your RP (.cer files).

- [Production environment](https://raw.github.com/WindowsAzure/azure-resource-provider-sdk/master/docs/misc/AzureStoreProduction.cer)
- [Stage environment](https://raw.github.com/WindowsAzure/azure-resource-provider-sdk/master/docs/misc/AzureStoreStage.cer)
- [Test environment](https://raw.github.com/WindowsAzure/azure-resource-provider-sdk/master/docs/misc/AzureStoreTest.cer)


###Subscription Lifecycle Events

When a user purchases a specific _Service Plan_ with our Add-on, Windows Azure will start sending your RP _subscription lifecycle events_ for the resource created. For example, if a user purchases the Add-on Clouditrace on the "Bronze" _Service Plan_, the Clouditrace RP will start receiving _subscription lifecycle events_ for that _Service Plan_ so that your service can take the appropriate action. 

Your RP will need to handle the following four _subscription lifecycle events_:

- [Create Resource](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/api-resource-create.md). This happens when a user purchases your Add-on from the Windows Azure Store. This is a `PUT` on a Resource.
- [Get Resource](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/api-resource-get.md). This happens when a user views details about a purchased Resource. This happens as a `GET` on the Resource's parent CloudService.
- [Delete Resource](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/api-resource-delete.md). This happens when a user deletes a previously-purchased Resource. This happens as a `DELETE` on a Resource or its parent CloudService.
- [Upgrade Resource](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/api-resource-upgrade.md). This happens when a user upgrades a _Service Plan_ for a previously-purchased Resource, from a lower tier (e.g. free) to a higher tier. This happens as a `PUT` on the Resource.

***NOTE:***The Resource Provider API uses the term _subscription_ to mean the recurring purchase of an Add-on's _Service Plan_, and should not be confused with Windows Azure subscriptions. 

####Request

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

- `EventId` is the ID of the subscription. **This field is deprecated and should not be used**.
- `EntityType` will always be _Subscription_. **This field can be ignored**.
- `EntityId/Id` is the ID of the subscription. It is a GUID, and should be stored by your service. Note that this is the Subscription ID and should be recorded by your service.
- `EntityEvent/EntityState` is the actual event. It can take four values: `Registered`, `Disabled`, `Enabled`, `Deleted`.
  - `Registered` This tells the RP that the user intends to create a resource under this subscription.
  - `Disabled` The user's Windows Azure subscription has been disabled, due to fraud or non-payment. Your RP should make the resource inaccessible without deleting its data.
  - `Enabled` The user's Windows Azure subscription has been enabled, because it is current on payments. Your RP should restore access to data.
  - `Deleted` The user's Windows Azure subscription has been deleted. Windows Azure retains data for 90 days. We recommend a similar retention policy.
- `OperationId` is a unique identifier for this subscription lifecycle event. It is similar in spirit to the ETag, because a subscription lifecycle event that is not acknowledged with an HTTP status code `200` or `201` will be retried again with the same `OperationId`.
- `Properties` is a property bag that Windows Azure passes to the RP. Only two properties are supported today:
  - `EMail` is the e-mail address of the logged-in user.
  - `OptIn` indicates whether the user has agreed to give you additional permissions about sending them marketing material. Your RP can always send transactional e-mails e.g. about service or account issues to the e-mail address given in the `EMail` field.

####Response

If the event is processed successfully, your RP should return a `200` or `201` HTTP status code.


###Single Sign-on (SSO)

In addition to supporting _resource lifecycle events_, your Add-on will need to support [SSO](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/api-sso.md). The Windows Azure Management Portal allows a user to select a previously-purchased Resource, and click the _Manage_ button. This signs the user into a service management dashboard hosted by the Add-on provider, without requiring the user to enter a username and password.

