Tips and Tricks
===

Tags need to be alphabetically sorted
---
The order of tags in your XML response matters: **all tags must always be alphabetically ordered, from A-Z**. For example, this response to GET on a Resource will fail:

```
<Resource xmlns=""http://schemas.microsoft.com/windowsazure">
	<ETag>decac2dc-879a-455a-9f00-30559ab06d3c</ETag>
	</IntrinsicSettings>
	<Plan>free_clouditrace</Plan>
	<SchemaVersion>1.0</SchemaVersion>
	<Type>monitoring</Type>
	<CloudServiceSettings>
		<GeoRegion>West US</GeoRegion>
	</CloudServiceSettings>
</Resource>
```
Can you see why? It's because the `CloudServiceSettings` node is not in the correct alphabetical order. This response will succeed:

```
<Resource xmlns="http://schemas.microsoft.com/windowsazure">
	<CloudServiceSettings>
		<GeoRegion>West US</GeoRegion>
	</CloudServiceSettings>
	<ETag>decac2dc-879a-455a-9f00-30559ab06d3c</ETag>
	</IntrinsicSettings>
	<Plan>free_clouditrace</Plan>
	<SchemaVersion>1.0</SchemaVersion>
	<Type>monitoring</Type>
</Resource>
```

ETag must be roundtripped
---
Windows Azure uses ETags to cache responses. When a resource is created, the ETag must be roundripped back in the response. Keep in mind that if Windows Azure receives an error, it will retry the operation with the same ETag several times.

OutputItems only need to be returned when a Resource is first created
---
Your RP may return `OutputItems`, which define information such as API keys and endpoints which can be used to connect to your service. If `OutputItems` are defined in your RP's [manifest](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/concepts.md), they must be returned when the Resource is created.

However, they do not need to be returned on subsequent GETs on the Resource or CloudService, as Windows Azure will cache `OutputItems`. If the user changes the value of the `OutputItem` e.g. changes a database password, you can return `OutputItems` with a new `ETag`. 


XML response must contain a namespace
---
The response XML must contain a namespace: `http://schemas.microsoft.com/windowsazure`, otherwise Windows Azure will not process it.

Your RP gets a modified Subscription ID
---
Your Resource Provider does not receive the actual ID of the Subscription as it is shown in the [Account Portal](https://account.windowsazure.com). For privacy reasons, Windows Azure sends you a mapped Subscription ID which does not show up in any Microsoft portal. You may run into this while debugging your RP in production.

Dates and times are in ISO-8601 format
---
Windows Azure provides dates and times in [ISO 8601](http://en.wikipedia.org/wiki/ISO_8601) format. The timezone is UTC.