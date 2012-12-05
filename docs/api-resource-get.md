Resource: Get Resource
===
Once a Resource has been provisioned, Windows Azure will call your endpoint to retrieve information about it. Typically, this will happen when a user goes to the [Management Portal](https://manage.windowsazure.com) and clicks on the Resource to view its details.

Request
---
In order to get details on a Resource, Windows Azure will do a `GET` on the parent CloudService.

URL:

`https://<base_uri>/subscriptions/<subscription_id>/cloudservices/<cloud_service_name>/`

Method: `GET`

Response
---
If the Resource or CloudService exists, your RP should return a `200` or `201` HTTP status code. Otherwise, return a `404`.

The response to a `GET` on a CloudService should be like this:

```xml
<CloudService xmlns="http://schemas.microsoft.com/windowsazure">
	<Resources>
		<Resource>
			<ETag>100-100-10203-302012</ETag>
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
					<Name>Servers</Name>
					<Included>5</Included>
					<Used>1</Included>
					<Unit>generic</Included>
				</UsageMeter>	
			</UsageMeters>
		</Resource>
			<Resource>
				<ETag>520-100-10203-302012</ETag>
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
						<Name>Servers</Name>
						<Included>10</Included>
						<Used>2</Included>
						<Unit>generic</Included>
				</UsageMeter>	
			</UsageMeters>
		</Resource>
	</Resources>
</CloudService>
```

The data under the `<Resource>` node should be as it is described in [Create Resource](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/api-resource-create.md), with an important exception: **OutputItems should not be returned since Windows Azure has already cached them.**
