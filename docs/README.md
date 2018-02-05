# Resource Provider API Guide

A _Resource Provider_ (RP) is the web service that allows users to purchase an Add-on from the Azure Store and then manage it from within the Azure Management Portal.  Each Add-on in the Azure Store needs an RP to communicate with the Azure platform in order to support the various workflows involved in supporting an Add-on in the Store.

An RP needs to support the following workflows:
- [Subscription Operations](#subscription-operations)
- [Resource Operations](#resource-operations)
- [Single Sign-On](#single-sign-on-operations)

***Please Note:*** the Azure Store is currently in Preview and we are actively improving the Resource Provider API based on feedback. Please make sure you read these  [important tips and gotchas](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/tips-and-tricks.md) before you start implementing your own RP.

To better understand this documentation, please read [Azure Platform Concepts](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/concepts.md) to understand the definitions and concept mappings for the Azure platform and Resource Provider API.

## Resource Provider API Documentation

The Resource Provider (RP) API is:

- HTTP RESTful, using verbs like GET, PUT, DELETE to manage resources
- XML-based. There is no support for JSON yet.
- Authentication is through X.509 certificates.

### Handling Requests

#### Endpoints
You should expect Requests on two endpoints defined in the Publisher Portal:

- <provisioning_endpoint> handles Requests from Azure in response to [Subscription Operations](#subscription-operations) and [Resource Operations](#resource-operations).  e.g. `https://<your_domain>/azurestore`.
- <sso_endpoint> handles [Single Sign-On](#single-sign-on) workflow. e.g. `https://<your_domain>/azurestore/sso`.

#### Headers
You should expect two headers. The `content-type` header will be set to `application/xml`. The `x-ms-version` header will be set to `2012-03-01` or later.

#### ETags
You are expected to keep track of ETags since Azure will retry failed operations with the same ETag.  ETags in Request and Response bodies allows Azure to cache your results. Read more about [Change Management using ETags](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/etags.md).

### Making Responses
Your RP should respond in less than 20 seconds to requests, otherwise Azure will consider the operation timed out.

Responses adhere to standard HTTP conventions. For simplicity, HTTP codes `200` and `201` are considered equivalent. `403` is used to indicated unauthorized access. `409`, codes in the `5xx` range and timeouts are considered errors, and Azure will retry with the same ETag.

Where a response body is required, you are expected to return XML. JSON is not currently supported, but is being considered for future versions of the API.

Make sure to set the `content-type` header to `application/xml`.

If your response size is greater than 1 MB, you will receive an HTTP code `500`.

Generally, case matters everywhere e.g. `started != Started`

### Authentication
The RP API is one-way, i.e. Azure can call your service, but your service cannot call Azure. All calls are made over HTTPS.

You are responsible for verifying the caller's certificate thumbprint. **Only accept calls from certificates that have the correct public key**.

Below certificate is used by Azure to call your RP (.cer file). This certificate is used for both Staging as well as Production.

- [Production\Stage environment](https://github.com/Azure/azure-resource-provider-sdk/blob/master/docs/misc/AzureStoreLatest.cer)

### Subscription Operations

When a user purchases a specific _Service Plan_ with our Add-on, Azure will start sending your RP _subscription lifecycle events_ for the resource created. For example, if a user purchases the Add-on "Contoso" using the "Bronze" _Service Plan_, the Contoso RP will start receiving _subscription lifecycle events_ for that _Service Plan_ so that your service can take the appropriate action. 

To state this another way, _subscription lifecycle events_ occur based on resource operations performed by your customer.  E.g. Your RP will receive a subscription `Registered` event for each Subscription before the first Resource is provisioned. This will be a "POST" Request. Once that is complete a provision Request will start.


An RP will need to handle four _subscription lifecycle events_, identified by the 'EntityState' field in the Request from Azure:
- `Registered` The user intends to purchase a _Service Plan_ under this Azure subscription.
- `Disabled` The user's Azure subscription has been disabled, due to fraud or non-payment. Your RP should make the resource inaccessible without deleting its data.
- `Enabled` The user's Azure subscription has been enabled, because it is current on payments. Your RP should restore access to data.
- `Deleted` The user's Azure subscription has been deleted. Azure retains data for 90 days. We recommend a similar retention policy.

#### Subscription Operation Request

URL: `<provisioning_endpoint>/subscriptions/<subscription_id>/Events`

Method: `POST` (all four _subscription lifecycle events_ use POST)

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
- `EntityId/Id` is the ID of the subscription, or _Subscription ID_. It is a GUID, and should be stored by your service. 
- `EntityEvent/EntityState` is the _subscription lifecycle event_. It can take four values: `Registered`, `Disabled`, `Enabled`, `Deleted`.
  - `Registered` The user intends to purchase a _Service Plan_ under this Azure subscription.
  - `Disabled` The user's Azure subscription has been disabled, due to fraud or non-payment. Your RP should make the resource inaccessible without deleting its data.
  - `Enabled` The user's Azure subscription has been enabled, because it is current on payments. Your RP should restore access to data.
  - `Deleted` The user's Azure subscription has been deleted. Azure retains data for 90 days. We recommend a similar retention policy.
- `OperationId` is a unique identifier for this subscription lifecycle event. It is similar in spirit to the ETag, because a subscription lifecycle event that is not acknowledged with an HTTP status code `200` or `201` will be retried again with the same `OperationId`.
- `Properties` is a property collection that Azure passes to the RP. Only two properties are supported today:
  - `EMail` is the e-mail address of the logged-in user.
  - `OptIn` indicates whether the user has agreed to give you additional permissions about sending them marketing material. Your RP can always send transactional e-mails e.g. about service or account issues to the e-mail address given in the `EMail` field.

#### Subscription Operation Response

If the event is processed successfully, your RP should return a `200` or `201` HTTP status code.

### Resource Operations

An RP will need to handle five different Requests that correspond to basic actions that a user performs on an Add-on resource from within the Azure Management Portal: 

- [Create Resource](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/api-create-resource.md). This happens when a user purchases your Add-on from the Azure Store. This is a `PUT` on a Resource.
- [Get Resource](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/api-get-resource.md). This happens when a user views details about a specific purchased Resource. This happens as a `GET` on the Resource.
- [Get Resources](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/api-get-resources.md). This happens when a user views details about purchased Resources for a CloudService. This happens as a `GET` on the Resource's parent CloudService.
- [Delete Resource](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/api-delete-resource.md). This happens when a user deletes a previously-purchased Resource. This happens as a `DELETE` on a Resource or its parent CloudService.
- [Upgrade Resource](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/api-upgrade-resource.md). This happens when a user upgrades a _Service Plan_ for a previously-purchased Resource, from a lower tier (e.g. free) to a higher tier. This happens as a `PUT` on the Resource.

### Single Sign-On Operations

In addition to supporting Subscription and Resource Operations, your Add-on will need to support [SSO Operations](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/api-sso.md). The Azure Management Portal allows a user to select a previously-purchased Resource, and click the _Manage_ button. This signs the user into a service management dashboard hosted by the Add-on provider, without requiring the user to enter a username and password.
