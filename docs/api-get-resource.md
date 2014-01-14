#Resource Operation: Get Resource

Windows Azure will call this endpoint to retrieve information about a single resource. Typically, this will happen when a user goes to the [Management Portal](https://manage.windowsazure.com) and clicks on the Resource to view its details.

##Request
In order to get details on a Resource, Windows Azure will do a `GET` for that particular resource.

URL:

`https://<base_uri>/subscriptions/<subscription_id>/cloudservices/<cloud_service_name>/resources/<resource_type>/<resourceName>`

Method: `GET`

##Response
If the Resource exists, your RP should return a `200` or `201` HTTP status code. Otherwise, return a `404`.

The response to a `GET` on a Resource should be like this:

```xml
<Resource xmlns="http://schemas.microsoft.com/windowsazure">
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
			<Included>5</Included>
			<Name>Servers</Name>
			<Unit>generic</Included>
			<Used>1</Included>
		</UsageMeter>	
	</UsageMeters>
</Resource>
```
