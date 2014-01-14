# Resource Provider API Guide

A _Resource Provider_ (RP) is a web service that allows users to purchase an Add-on from the Windows Azure Store and manage it from within the Windows Azure Management Portal.  Each Add-on in the Windows Azure Store has it's own Resource Provider that communicates with the Windows Azure platform, in order to support the various workflows involved in supporting an Add-on in the Store.

***Please Note:*** the Windows Azure Store is currently in Preview and we are actively improving the Resource Provider API based on feedback. Please make sure you read these  [important tips and gotchas](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/tips-and-tricks.md) before you start implementing your own RP.

Read [Concepts](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/concepts.md) to understand the definitions and concept mappings for the Windows Azure platform and Resource Provider API.

##API Documentation
- [API Overview](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/api-overview.md)
- [Subscription Events API](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/api-subscription.md)

Your RP will receive calls from the Windows Azure platform (for Resource creation, Resource deletion, etc.) on the base URI defined in the Publisher Portal. Your RP will need to handle the following events on a Resource:

- [Create Resource](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/api-resource-create.md). This happens when a user purchases your Add-on from the Windows Azure Store. This is a `PUT` on a Resource.
- [Get Resource](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/api-resource-get.md). This happens when a user views details about a purchased Resource. This happens as a `GET` on the Resource's parent CloudService.
- [Delete Resource](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/api-resource-delete.md). This happens when a user deletes a previously-purchased Resource. This happens as a `DELETE` on a Resource or its parent CloudService.
- [Upgrade Resource](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/api-resource-upgrade.md). This happens when a user upgrades a _Service Plan_ for a previously-purchased Resource, from a lower tier (e.g. free) to a higher tier. This happens as a `PUT` on the Resource.

In addition, your Add-on will need to support [SSO](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/api-sso.md). The Windows Azure Management Portal allows a user to select a previously-purchased Resource, and click the _Manage_ button. This signs the user into a service management dashboard hosted by the Add-on provider, without requiring the user to enter a username and password.

