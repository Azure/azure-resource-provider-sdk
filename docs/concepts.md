#Azure Platform Concepts

A Resource Provider (RP, for short) is simply an HTTPS RESTful API contract that Add-on owners will implement so a trusted Azure endpoint can provision, delete, and manage services on a user's behalf. Azure uses the Response from an RP to render and show a set of simple management operations in the Azure Management Portal.

The figure below gives a simplified view of how a user interacts directly with Azure through the Azure Management Portal, PowerShell scripts or *NIX command-line tools. Azure, in turn, communicates with your RP to manage the user's service.

![overview](https://raw.github.com/WindowsAzure/azure-resource-provider-sdk/master/docs/images/arch-overview.png)

##Azure Concepts
Before we dive into RP concepts, it will be helpful to understand several Azure concepts first. 

- Every user who signs up for Azure logs in with a Microsoft account (e.g. abby@live.com or bob@hotmail.com).

- The user then creates a Azure **Subscription**.  A Subscription is a named entity e.g. _3-month Free Trial_ or _MyApp Production_ associated with billing information. You can view your own Subscriptions on the [Account Portal](https://account.windowsazure.com).

- Next, the user creates one or more **Resources** such as a Website, Virtual Machine or Add-on. Website and Virtual Machine are two different **ResourceTypes**. Each Resource is deployed under exactly one Azure Subscription.

This is a conceptual view of a user's Resources:

* There are two Subscriptions, _Subscription A_ and _Subscription B_.
* Subscription A has two Resources, named _Resource 1_ and _Resource 2_.
* Subscription B has one Resource, named _Resource 1_. 

![resources](https://raw.github.com/WindowsAzure/azure-resource-provider-sdk/master/docs/images/arch-resources.png)

##Resource Provider Concepts
- Each Resource's lifecycle is managed by a **ResourceProvider**. This is a common software design pattern, where a manager / orchestrator (Azure) relies on a provider (ResourceProvider) to provide specific functionality.

- An RP introduces an additional concept, called a **CloudService**. Instead of nesting a Resource directly under a Subscription, Resources are nested under a named entity called a CloudService. Think of a CloudService as a container of resources, roughly analogous to an application.

Tying it together, this is a conceptual view of the user's resources:

![rp](https://raw.github.com/WindowsAzure/azure-resource-provider-sdk/master/docs/images/arch-cloud-services.png)

* There are two Subscriptions, _Subscription A_ and _Subscription B_.
* Subscription A has two CloudServices, named _CloudService X_ and _CloudService Y_.
   * _CloudService X_ has a single Resource, named _Resource 1_.
   * _CloudService Y_ has a single Resource, named _Resource 2_. This Resource is provided by a Resource Provider named 'clouditrace' which exposes a single Resource of type 'monitoring'. Note that the combination of Subscription ID, Cloud Service ID and Resource Name must be unique.
* Subscription B has a single CloudService, named _Cloud Service X_ with a single Resource, named _Resource 1_.

![together](https://raw.github.com/WindowsAzure/azure-resource-provider-sdk/master/docs/images/arch-together.png)