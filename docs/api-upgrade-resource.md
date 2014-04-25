#Resource Operation: Upgrade Resource

If your service offers multiple plans or tiers (e.g. Free, Silver, Gold), users can freely move to higher tiers from the [Management Portal](https://manage.windowsazure.com). Your RP will receive a `POST` on a Resource when this happens.

##Request
URL: `<provisioning_endpoint>/subscriptions/<subscription_id>/cloudservices/<cloud_service_name>/resources/<resource_type>/<resource_name>`

Method: `POST`

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
The payload of this file is identical to what is received in [Create Resource](https://github.com/Azure/azure-resource-provider-sdk/tree/master/docs/api-create-resource.md). However, the `Plan` node has the new plan's value.

##Response
If the Resource was upraded provisioned, return a `200` or `201` HTTP status code with an XML body representing the Resource, as defined in [Get Resource](https://github.com/Azure/azure-resource-provider-sdk/tree/master/docs/api-get-resource.md).

If the upgrade failed e.g. with an HTTP status code `500`, Azure will retry the upgrade.
