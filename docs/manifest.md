Resource Provider Manifest
===
While registering your Resource Provider and its offering on the [Publishing Portal](http://publish.marketplace.windowsazure.com), you will be required to provide an XML manifest describing how Windows Azure connects to your RP, and what data it expects to receive from it.

```xml
<ResourceManifest>
	<Test>
		<ResourceProviderEndpoint>https://staging.contoso.com</ResourceProviderEndpoint>
		<ResourceProviderSsoEndpoint>https://staging.contoso.com/sso</ResourceProviderSsoEndpoint>
	</Test>
	<Prod>
		<ResourceProviderEndpoint>https://production.contoso.com</ResourceProviderEndpoint>
		<ResourceProviderSsoEndpoint>https://production.contoso.com/sso</ResourceProviderSsoEndpoint>
	</Prod>
	<OutputKeys>
		<OutputKey>
			<Name>username</Name>
		</OutputKey>
		<OutputKey>
			<Name>password</Name>
		</OutputKey>
	</OutputKeys>
</ResourceManifest>
```

The first two sections of the manifest, `Test` and `Prod` describe how Windows Azure will connect to your RP's test and production endpoints. Real users will never connect to your test endpoints, but Microsoft will use them for signoff. **Both of these sections are required**.

`ResourceProviderEndpoint` is the HTTPS endpoint where Windows Azure will send Subscription lifecycle events, and Resource create, get, delete, upgrade requests. 

`ResourceProviderSsoEndpoint` is where Windows Azure will send users who are logging into your management dashboard using the [SSO](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/api-sso.md) mechanism. **Both of these fields are required**.

`OutputKeys` are described in detail in [Create Resource](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/api-resource-create.md). They must be defined here, since Windows Azure will cache returned values. **OutputKeys are optional but if you do not have OutputKeys, leave an empty <OutputKeys/> node.**
