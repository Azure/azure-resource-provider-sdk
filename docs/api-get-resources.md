#Resource Operation: Get Resources
Once a Resource has been provisioned, Azure will call your endpoint to retrieve information about it. Typically, this will happen when a user goes to the [Management Portal](https://manage.windowsazure.com) and clicks on the Resource to view its details.

##Request
In order to get details on a Resource, Azure will do a `GET` on the parent CloudService.

URL:

`<provisioning_endpoint>/subscriptions/<subscription_id>/cloudservices/<cloud_service_name>/`

Method: `GET`

##Response
If the Resource or CloudService exists, your RP should return a `200` or `201` HTTP status code. Otherwise, return a `404`.

The response to a `GET` on a CloudService should be like this:

```xml
<CloudService xmlns="http://schemas.microsoft.com/windowsazure">
	<GeoRegion>West US</GeoRegion>
	<Resources>
		<Resource>
			<ETag>A71D8BD1-9D4A-48A9-9591-DEA26651BE24</ETag>
			<Name>helloworld</Name>
			<OperationStatus>
				<Result>Succeeded</Result>
			</OperationStatus>
			<Plan>free</Plan>
			<State>Started</State>
			<SubState>Waiting for your calls</SubState>
			<Type>monitoring</Type>
			<UsageMeters>
				<UsageMeter>
					<Included>5</Included>
					<Name>Servers</Name>
					<Unit>generic</Unit>
					<Used>1</Used>
				</UsageMeter>
			</UsageMeters>
		</Resource>
		<Resource>
			<ETag>526FF5B9-16D3-4272-82EB-D92DD498940F</ETag>
			<Name>myresource</Name>
			<OperationStatus>
				<Result>Succeeded</Result>
			</OperationStatus>
			<Plan>silver</Plan>
			<State>Started</State>
			<SubState>Waiting for your calls</SubState>
			<Type>monitoring</Type>
			<UsageMeters>
				<UsageMeter>
					<Included>10</Included>
					<Name>Servers</Name>
					<Unit>generic</Unit>
					<Used>2</Used>
				</UsageMeter>
			</UsageMeters>
		</Resource>
	</Resources>
</CloudService>
```

The data under the `<Resource>` node should be as it is described in [Create Resource](https://github.com/Azure/azure-resource-provider-sdk/tree/master/docs/api-resource-create.md), with two important exceptions:

- You don't need to include `CloudService` node under each `Resource`
- **OutputItems should not be returned since Azure has already cached them.**
