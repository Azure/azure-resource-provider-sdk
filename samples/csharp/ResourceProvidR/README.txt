Sample Windows Azure Resource Provider

* Urls to respond to:

		// -------- Subscription Notifications --------

		POST /subscriptions/{subscriptionId}/Events

		// -------- Cloud Services Management --------

		GET /subscriptions/{subscriptionId}/cloudservices
		GET /subscriptions/{subscriptionId}/cloudservices/{cloudServiceName}
		DELETE /subscriptions/{subscriptionId}/cloudservices/{cloudServiceName}

		// -------- Resource Management --------

		GET /subscriptions/{subscriptionId}/cloudservices/{cloudServiceName}/resources/{resourceName}
		PUT /subscriptions/{subscriptionId}/cloudservices/{cloudServiceName}/resources/{resourceName}
		DELETE subscriptions/{subscriptionId}/cloudservices/{cloudServiceName}/resources/{resourceName}