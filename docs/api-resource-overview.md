Resource API
===
Your RP will receive calls regarding resource creation, deletion etc. on the base URI defined in  the [manifest](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/manifest.md). Your RP will need to handle several different types of events on a Resource:

* [Create Resource](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/api-resource-create.md). This happens when a user purchases your offering from the Windows Azure Store. This is a `PUT` on a Resource.
* **Show Resource**. This happens when a user views details about a purchased Resource. This happens as a `GET` on a Resource or its parent CloudService.
* **Delete Resource**. This happens when a user deletes a previously-purchased Resource. This happens as a `DELETE` on a Resource or its parent CloudService.
* **Upgrade Resource**. This happens when a user upgrades a plan for a previously-purchased Resource, from a lower tier (e.g. free) to a higher tier. _Downgrades are not currently supported_. This happens as a `PUT` on the Resource.