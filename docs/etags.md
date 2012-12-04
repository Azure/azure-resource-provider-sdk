ETags
===
Windows Azure uses [ETags](http://en.wikipedia.org/wiki/HTTP_ETag) for efficient caching of responses. ETags are used because Windows Azure may send the same request more than once. Two requests with the same ETag indicate the same operation.

ETags are used in several scenarios. For example:

* *Retries*. If a subscription lifecycle event fails, Windows Azure will retry it multiple times with the same ETag.
* *Caching*. Windows Azure will cache the response of your resource's OutputItems. If you change their value out-of-band e.g. a user changes their database password, you can return the OutputItems with a different ETag on a Get Resource, and Windows Azure will update its cache.