Dukaan: Testing your Resource Provider locally
===

_Dukaan_ is a tool for testing your Resource Provider locally, without having to use the [Management Portal](https://manage.windowsazure.com) to purchase your add-on. This enables you to rapidly iterate on your code by testing Create Resource, Show Resource, etc., without having to make tedious, manual purchases in the UI.

Requirements
---
Dukaan can run on any OS that supports [Python 2.7](http://www.python.org).

Installation
---
The recommended way to install Dukaan is using [pip](http://pypi.python.org/pypi/pip):

```
pip install dukaan

```

Initialization
---
Dukaan stores frequently-used settings in a configuration file, which makes commands shorter by providing sensible defaults. To setup or change values in the configuration file, run this command:


```
dukaan init
``` 

Dukaan will now prompt you for several values:

* **Resource Provider Namespace**: This is the value you entered in the Publisher Portal during initial registration. Typically, this is your company's name. E.g. 'contoso'. Please refer to the [Publisher Portal Guide](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/publisher-portal.md) for more details.
* **Resource Type**: This is the Resource Type you entered for your RP in the Publisher Portal. Please refer to the [Publisher Portal Guide](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/publisher-portal.md) for more details.
* **Subscription ID**: This is the Subscription under which Resources will be created, deleted, etc. A good default is _my_subscription_.
* **Resource Name**: This is the name of the Resource to create, delete, etc. A good default is _my_resource_.
* **Base Plan Name**: This is the ID of the plan that will be used for the Create Resource test. **Enter the ID as your code expects to see it, not the user-friendly name e.g. contoso_10_gb, not _Contoso Silver 10 GB** You entered this value in the _Plan_ section of the Publisher Portal. Please refer to the [Publisher Portal Guide](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/publisher-portal.md) for more details.
* **Upgrade Plan Name**: This is the ID of the plan that will be used for the Upgrade Resource test. **Enter the ID as your code expects to see it, not the user-friendly name e.g. contoso_10_gb, not _Contoso Silver 10 GB** You entered this value in the _Plan_ section of the Publisher Portal. Please refer to the [Publisher Portal Guide](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/publisher-portal.md) for more details.

The Manifest
---
Dukaan uses the [manifest](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/manifest.md) to determine what endpoints to connect to. For local testing, a manifest like this will suffice (note that the `Test` environment points to the local development web server over HTTP):

```
<ResourceManifest>
	<Test>
		<ResourceProviderEndpoint>http://localhost:5000</ResourceProviderEndpoint>
		<ResourceProviderSsoEndpoint>http://localhost:5000</ResourceProviderSsoEndpoint>
	</Test>
	<Prod>
		<ResourceProviderEndpoint>http://production.contoso.com</ResourceProviderEndpoint>
		<ResourceProviderSsoEndpoint>http://production.contoso.com/sso</ResourceProviderSsoEndpoint>
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

If your manifest is not located in the working directory where Dukaan is run, use the `--manifest` flag to specify the absolute path.

Testing the manifest
---
The first test you should probably run is to test the manifest:

```
dukaan manifest
```

You may see some warnings, especially during development. Make sure you fix them before you upload the manifest using the Publisher Portal.

```
    [WARN] Manifest: Base URI for Test environment is not HTTPS
    [WARN] Manifest: SSO URI for Test environment is not HTTPS
    [WARN] Manifest: Base URI for Prod environment is not HTTPS
    [WARN] Manifest: SSO URI for Prod environment is not HTTPS
```

Testing Create Resource
---
To test [Create Resource](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/api-resource-create.md), run this command:

```
dukaan create
```

If everything goes well, you should see this output with `INFO` and `PASS` line items only:

```
    [INFO] POST on http://localhost:5000/subscriptions/my_subscription/Events
    [INFO] Server returned HTTP status code 200
    [PASS] Subscription register event succeeded
    [INFO] PUT on http://localhost:5000/subscriptions/my_subscription/cloudservices/Azure-Stores-MOES3Y8O4S5PKQ5OI4TK1VB7U6ZON95KZXV0YUA0ZGWCADRO4NS4-Northwest-US/resources/monitoring/my_resource
    [INFO] Server returned HTTP status code 200
    [PASS] Resource creation succeeded
    [INFO] Checking XML
    [INFO] Checking if root node's tag is {http://schemas.microsoft.com/windowsazure}Resource
    [INFO] Checking if CloudServiceSettings are present
    [INFO] Checking if ETag is d001e242-424f-11e2-a4c1-20c9d048bc89
    [INFO] Checking if Name is my_resource
    [INFO] Checking if OperationStatus/Result is 'Succeeded'
    [INFO] Checking if OutputItems are present
    [INFO] Checking if UsageMeters are present
    [INFO] Checking if Plan is present
    [INFO] Checking if State is 'Started'

```

Testing Show Resource
---
To test [Show Resource](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/api-resource-get.md), run this command:

```
dukaan get
```

If everything goes well, you should see this output with `INFO` and `PASS` line items only:

```
    [INFO] GET on http://localhost:5000/subscriptions/my_subscription/cloudservices/Azure-Stores-MOES3Y8O4S5PKQ5OI4TK1VB7U6ZON95KZXV0YUA0ZGWCADRO4NS4-Northwest-US
    [INFO] Server returned HTTP status code 200
    [PASS] Get CloudService succeeded.
    [INFO] Checking XML
```

Testing Upgrade Resource
---
To test [Upgrade Resource](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/api-resource-upgrade.md), run this command:

```
dukaan upgrade
```

If everything goes well, you should see this output with `INFO` and `PASS` line items only:

```
    [INFO] PUT on http://localhost:5000/subscriptions/my_subscription/cloudservices/Azure-Stores-MOES3Y8O4S5PKQ5OI4TK1VB7U6ZON95KZXV0YUA0ZGWCADRO4NS4-Northwest-US/resources/monitoring/my_resource
    [INFO] Server returned HTTP status code 200
    [PASS] Upgrade Resource succeeded.
    [INFO] Checking XML
    [INFO] Checking if root node's tag is {http://schemas.microsoft.com/windowsazure}Resource
    [INFO] Checking if CloudServiceSettings are present
    [INFO] Checking if ETag is 48aef326-4250-11e2-83ae-20c9d048bc89
    [INFO] Checking if Name is my_resource
    [INFO] Checking if OperationStatus/Result is 'Succeeded'
    [INFO] Checking if OutputItems are present
    [INFO] Checking if UsageMeters are present
    [INFO] Checking if Plan is present
    [INFO] Checking if State is 'Started'
    [INFO] Checking if new plan is gold
```

Testing SSO
---
To test [SSO](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/sso.md), run this command:

```
dukaan sso
```

Dukaan will test SSO with a valid timestamp, and with an invalid timestamp. Your code must past both tests, otherwise you will see errors:

```
SO with valid timestamp and token

    [INFO] POST on http://localhost:5000/subscriptions/my_subscription/cloudservices/Azure-Stores-MOES3Y8O4S5PKQ5OI4TK1VB7U6ZON95KZXV0YUA0ZGWCADRO4NS4-Northwest-US/resources/monitoring/my_resource/SsoToken
    [INFO] Server returned HTTP status code 200
    [PASS] SSO token request succeeded.
    [INFO] Checking XML
    [INFO] GET on http://localhost:5000/sso?subid=my_subscription&cloudservicename=Azure-Stores-MOES3Y8O4S5PKQ5OI4TK1VB7U6ZON95KZXV0YUA0ZGWCADRO4NS4-Northwest-US&resourcetype=monitoring&resourcename=my_resource&timestamp=2012-12-09+14%3A35%3A33.261637&token=731855c057e7947c2ab7b5613e25b2b8d8f3d91a
    [INFO] Server returned HTTP status code 200
    [PASS] SSO login succeeded.

SSO with expired timestamp

    [INFO] GET on http://localhost:5000/sso?subid=my_subscription&cloudservicename=Azure-Stores-MOES3Y8O4S5PKQ5OI4TK1VB7U6ZON95KZXV0YUA0ZGWCADRO4NS4-Northwest-US&resourcetype=monitoring&resourcename=my_resource&timestamp=2012-12-09+14%3A45%3A33.261637%2B00%3A00&token=731855c057e7947c2ab7b5613e25b2b8d8f3d91a
    [INFO] Server returned HTTP status code 200

```