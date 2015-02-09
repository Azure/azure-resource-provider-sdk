#Change Management using ETags
Azure uses [ETags](http://en.wikipedia.org/wiki/HTTP_ETag) for efficient caching of responses. ETags are used because Azure may send the same request more than once. Two requests with the same ETag indicate the same operation.  Azure ETags are [GUIDs](http://en.wikipedia.org/wiki/Globally_unique_identifier).

ETags are used in several scenarios. For example:

- *Retries*. If a [Subscription Operation](https://github.com/Azure/azure-resource-provider-sdk/tree/master/docs#subscription-operations) or [Resource Operation](https://github.com/Azure/azure-resource-provider-sdk/tree/master/docs#resource-operations) fails, Azure will retry the Request multiple times with the same ETag.
- *Caching*. Azure will cache the Response of your resource's OutputItems. If you change their value out-of-band (e.g. a user changes their database password), you can return the OutputItems with a different ETag on a Get Resource, and Azure will update its cache.