API Overview
===
The Resource Provider (RP) API is:

* HTTP RESTful, using verbs like GET, PUT, DELETE to manage resources
* XML-based. There is no support for JSON yet.
* Authentication is through X.509 certificates.

Handling requests
---
You should expect requests on two endpoints defined in your offer's [manifest](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/manifest.md). You will receive resource lifecycle requests such as create, delete, update etc. on the *base URL* `https://www.clouditrace.com/azurestore`. Single sign-on requests will come on the *SSO URL* defined in the manifest, e.g. `https://www.clouditrace.com/azurestore/sso`.

Requests will be made in XML. JSON is not currently supported, but is being considered for future revs of the API.

You should expect two headers. The `content-type` header will be set to `application/xml`. The `x-ms-version` header will be set to `2012-03-01` or later.

[ETags](http://en.wikipedia.org/wiki/HTTP_ETag) in request and response bodies allow Windows Azure to cache your results. Windows Azure ETags are [GUIDs](http://en.wikipedia.org/wiki/Globally_unique_identifier). You are expected to keep track of ETags beacause Windows Azure will retry failed operations with the same ETag.

Making responses
---
Your RP should respond in less than 20 seconds to requests, otherwise Windows Azure will consider the operation timed out.

Responses adhere to standard HTTP conventions. For simplicity, HTTP codes `200` and `201` are considered equivalent. `403` is used to indicated unauthorized access. `409`, codes in the `5xx` range and timeouts are considered errors, and Windows Azure will retry with the same ETag.

Where a response body is required, you are expected to return XML. JSON is not currently supported, but is being considered for future revs of the API.

Make sure to set the `content-type` header to `application/xml`.

If your response size is greater than 1 MB, you will receive an HTTP code `500`.

Generally, case matters everywhere e.g. `started != Started`

Authentication
---
The RP API is one-way i.e. Windows Azure can call your service, but your service cannot call Windows Azure. All calls are made over HTTPS.

You are responsible for verifying the caller's certificate thumbprint. **Only acce*pt calls from certificates that have the correct public key**.

Below are the certificates used by Windows Azure to call into your RP (.cer files).

* [Production environment](https://raw.github.com/WindowsAzure/azure-resource-provider-sdk/master/docs/misc/AzureStoreProduction.cer)
* [Test environment](https://raw.github.com/WindowsAzure/azure-resource-provider-sdk/master/docs/misc/AzureStoreTest.cer)



