Resource API: Create Resource
===
Once a Subscription has received a `Registered` event, any user with Service Administrator or Co-Administrator role for that Subscription may create and manage CloudServices containing Resources implemented by the RP.

>Your RP will receive a subscription `Registered` event for each Subscription before the first Resource is provisioned.

Request
---
URL: `https://<base_uri>/subscriptions/<subscription_id>/cloudservices/<cloud_service_name>/resources/<resource_type>/<resource_name>`

Method: `PUT`

Sample:

```xml
<Resource xmlns="http://schemas.microsoft.com/windowsazure">
	<CloudServiceSettings>
		<GeoRegion>West US</GeoRegion>
	</CloudServiceSettings>
	<ETag>decac2dc-879a-455a-9f00-30559ab06d3c</ETag>
	<Plan>free</Plan>
	<PromotionCode/>
	<SchemaVersion>1.0</SchemaVersion>
	<Type>monitoring</Type>
</Resource>
```

* `CloudServiceSettings/GeoRegion` is **required** and it indicates the Windows Azure region the Resource should be provisioned in: `West US`, `East US`, `North Central US`, `South Central US`,  `West Europe`, `North Europe`, `East Asia`, `Southeast Asia`.
  * In case you provided a region list when registering your offering on the Publisher Portal, Windows Azure will only allow Resources to be created within that subset of regions.
  * If you have not provided any supported regions at the time of registration, send back the same value that you receive and ignore this value.
* `ETag` is a **required** field, described in [Change Management using ETags](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/etags.md).
* `Plan` is **required** and indicates the plan the user choose while purchasing your offering. This is one of the plan identifiers you entered in the Publisher Portal for your offering.
* `PromotionCode` is an **optional** field, and it is provided to you for analytics. When you create your offering in the Publisher Portal, you can define promotion codes which give discounts to users. These promotion codes are passed to you at time of purchase.
* `SchemaVersion` is an **optional** field that can be ignored by your RP.
* `Type` is a **required** field that indicates the Resource Type. It will be the value of `Resource Type` you entered in the Publishing Portal for your offering.


Response
---
If the Resource was successfully provisioned, return a `200` or `201` HTTP status code with an XML body:


```xml
<?xml version="1.0" encoding="UTF-8"?>
<Resource xmlns="http://schemas.microsoft.com/windowsazure">
	<CloudServiceSettings>	
			<GeoRegion>West US</GeoRegion>
	</CloudServiceSettings>	
	<ETag>decac2dc-879a-455a-9f00-30559ab06d3c</ETag>
	<Name>helloworld</Name>
	<OperationStatus>
		<Result>Succeeded</Result>
	</OperationStatus>
	<OutputItems>
		<OutputItem>
			<Key>username</Key>
			<Value>fake_user</Value>
		</OutputItem>
		<OutputItem>
			<Key>password</Key>
			<Value>fake_password</Value>
		</OutputItem>
	</OutputItems>
	<Plan>free</Plan>
	<State>Started</State>
	<SubState>Waiting for your API calls</SubState>
	<UsageMeters>
		<UsageMeter>
			<Name>Servers</Name>
			<Included>5</Included>
			<Used>1</Included>
			<Unit>generic</Included>
		</UsageMeter>	
	</UsageMeters>	
</Resource>
```
* `CloudServiceSettings/GeoRegion` is a **required** field. It should contain the geo-region your service is deployed in. If your service is not deployed in a Windows Azure geo-region, just return the value of the geo-region Windows Azure provisioned your Resource with.
* `ETag` is described in [Change Management using ETags](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/etags.md).
* `Name` is a **required** field. It isthe name of the Resource, as provided by the user.
* `OperationStatus/Result` is a **required** field, indicating the result of the create operation. It can take two values, `Succeeded` or `Failed`. If a failure happens, you can return additional information:

```xml
<OperationStatus>
	<Result>Failed</Result>
	<Error>
		<HttpCode>403</HttpCode>
		<Message>User is unauthorized to create this resource</Message>
	</Error>
</OperationStatus>

```

* `Error/HttpCode` should be used to further classify the error in the `4xx` range. This value may be displayed to client.
* `Error/Message` should be used to describe the error in detail. This value may be displayed to client.
* `OutputItems` is an **optional**  property bag used to send back key-value pairs users can use to connect to the Resource. You can only send back `OutputItems` that were registered in the [manifest](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/manifest.md). All of the below fields are **required**:
  * `Key` is a unique key identifying the `OutputItem` e.g. `username`
  * `Value` indicates the value associated with the key e.g. `john-doe`
* `Plan` is **required**, and it is the ID of the plan associated with the Resource e.g. `free`
* `State` is a **required** field, which takes one of these values:
  * `Started` indicates that the resource is working correctly 
  * `Stopped` indicates that the resource was stopped due to a user action
  * `Paused` indicates that the resource was temporarily put on hold
* `SubState` is an **optional** field, which your RP can use to return extra state information to Windows Azure.
* `UsageMeters` is an **optional** field, which your RP can use to return information about the quota usage. For example, if your RP provides a database-as-a-service, you can return information about number of connections and storage amount included and used by the Resource. All of the below fields are **required**:
  * `Name` is the name of the `UsageMeter` as it should be displayed to the user e.g. `Storage` or `Connections`
  * `Used` is the amount of the resource used e.g. 20 or 5.25. **This value must be parseable as a double**.
  * `Included` is the amount of the resource included in the plan e.g. 500 or 10.00. **This value must be parseable as a double**.
  * `Unit` is the unit that will be displayed in the Management Portal. Possible values are `bytes`, `hours` or `generic`. Be aware that these values have to be lower case. Use `generic` if you have a `UsageMeter` that does not map to storage space or time.
