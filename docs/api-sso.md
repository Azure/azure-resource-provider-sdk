Single Sign-on (SSO)
===
The [Management Portal](https://manage.microsoft.com) allows a user to select a previously-purchased Resource, and click the _Manage_ button. This signs the user into your service management dashboard, without requiring them to enter a username and password.

This functionality comes from your RP's implementation of a simple SSO protocol:

1. Windows Azure does a `POST` on `https://<base_url>/subscriptions/<subscription_id>/cloudservices/<cloud_service_name>/resources/<resource_type>/<resource_name>/SsoToken`.
2. Your RP takes the above parameters and concatenates them with a **secret that only you know**, and performs a [SHA-256 hash](http://en.wikipedia.org/wiki/SHA-2) of the concatenated string. In Python:

```python
	import hashlib
	secret = 'a_long_cryptic_secret_only_you_know'
	signature = "%s:%s:%s:%s:%s" % (subscription_id, cloud_service_name, resource_type, resource_name, secret)
	token = hashlib.sha256(signature)
```

and returns the following XML:

```xml
<SsoToken xmlns="http://schemas.microsoft.com/windowsazure">
	<TimeStamp>2012-10-05T05:09:03+00:00</TimeStamp>
	<Token>63e9a232b0bc8e5083571d1e72f58e5d670f6482</Token>
</SsoToken>
```

* `TimeStamp` is the current server datetime in [ISO-8601](http://en.wikipedia.org/wiki/ISO_8601) format in the server's own timezone.
* `Token` is the SHA-256 hash of the string `<subscription_id>:<cloud_service_name>:<resource_name>:<secret>`

3. The [Management Portal](https://manage.windowsazure.com) redirects the user to a URL to the SSO URL defined in the [manifest](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/manifest.md) with a few parameters:

`https://<sso_url>?token=<token>&subid=<subscription_id>&cloudservicename=<cloud_service_name>&resourcetype=<resource_type>&resourcename=<resource_name>`

4. Your RP generates the token again. If the token matches, and if the timestamp is within a 10 minute period, the RP sets a cookie and logs the user in. Otherwise, the RP returns a `403` error.

Sample code in Python with the Flask framework: 


```python
import hashlib
import iso8601

def sso_view():
	subscription_id = request.args.get("subid")
	cloud_service_name = request.args.get("cloudservicename")
	resource_name = request.args.get("resourcename")
	resource_type = request.args.get(resourcetype)
	timestamp = request.args.get("timestamp")
	
	secret = 'a_long_cryptic_secret_only_you_know'

	signature = "%s:%s:%s:%s:%s" % (subscription_id, cloud_service_name, resource_type, resource_name, secret)
	token_now = str(hashlib.sha256(signature).hexdigest())
	if (token_now == request.args.get("token")):
		app.logger.debug("Tokens match, checking timestamp")
		timestamp_now = datetime.now()
		timestamp_given = iso8601.parse_date(timestamp).replace(tzinfo=None)
		time_delta = timestamp_now - timestamp_given
		if(time_delta.seconds < 60*10):
			return Response("Welcome you are logged in", status=200)
		else:
			app.logger.debug("SSO error: Time delta greater 10 minutes")
			return Response("Login failed", status=403)
	else:
		app.logger.debug("SSO error: Given token %s does not match required token %s" % (request.args.get("token"), token_now))
		return Response("Login failed", status=403)
```

