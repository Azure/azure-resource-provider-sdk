# Windows Azure Store SDK

If you are looking for technical information and guides on how to integrate products and services with the [Windows Azure Store](http://www.windowsazure.com/en-us/store/overview/), you have come to the right place.  

![overview](https://raw.github.com/WindowsAzure/azure-resource-provider-sdk/master/docs/images/azure-store1.png)  

Included in this repo you will find:
- [Technical Documentation and Samples](https://github.com/WindowsAzure/azure-resource-provider-sdk/blob/master/README.md#technical-documentation-and-samples) for building a Resource Provider (web service) for the Windows Azure Store.
- An [Onboarding Guide](https://github.com/WindowsAzure/azure-resource-provider-sdk/blob/master/README.md#onboarding-guide) to walk you through all the steps required to get an Add-on into the Windows Azure Store; from creating your Seller Account with Microsoft, to releasing our Add-on into Production.
- An [FAQ](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/faq.md) to help answer your questions.

**Please note:** the Windows Azure Store is currently in Preview and this is a pre-release SDK and constantly evolving based on customer feedback.


## Onboarding Guide

**Step 1: Submit Microsoft Seller Application.**  You must be an approved seller in order to publish and Add-on in the Windows Azure Store and receive payout.  Note that if you have already released an app you may already be an approved seller.  You only need one approved seller account to sell apps and services in Microsoft Marketplaces.  Read the [Publisher Portal Guide](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/publisher-portal.md) to learn how to start the Seller Application process.

**Step 2: Create yYour Publisher Portal Account and Define Your Add-on.**  The Publisher Portal is how you will manage the details of your Add-on, including marketing copy, pricing and endpoints for your Resource Provider.  Read the [Publisher Portal Guide](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/publisher-portal.md) to get started.

**Step 3: Build and Test Your Resource Provider.**  A Resource Provider is the web service that will communicate with the Azure Store platform in order to support your Add-on.

**Step 4: Build the SSO Experience.** Your Add-on will need to support SSO from inside the Azure Managemetn Portal out to a page on your website (usually a dashboard so the user can further customize their Add-on).  Read our SSO guide (coming soon) to learn more about implementing SSO as well as our guidelines.

**Step 5: Publish Your Add-on to Preview.**  In order to test how your Add-on will look and work in the Windows Azure Store, we have a preview/test enviroment that using accounts with test billing info in order to fully test your Add-on.

**Step 6: Publish Your Add-on to Production.** Once your Add-on is tested and working in Preview, you will use the Publishing Portal to publish your Add-on to production.  This will initiate a final review process by Microsoft Store admins.  When your Add-on is approved it will be released to the live Windows Azure Store.

**Step 7: Schedule Co-marketing for Your Add-on.** Use some Windows Azure marketing muscle to grow awareness of your Add-on.  Read here (coming soon) about co-marketing opportunities.

**Step 8: Fine-tune Your Add-on.**  Unless you got it completely right the first time, you will want to use the Publisher Portal to adjust pricing and tiers, descriptions and make some promo codes.  Read here (coming soon) about how to make changes to your Add-on.

##Technical Documentation and Samples

**Please note:** the Windows Azure Store is currently in Preview and we are currently working on a new .NET SDK that will make it easy to quickly standup a Resource Provider for your Add-on.  We expect to release this new SDK before our Build conference in April.

- [API reference](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs)
- Code samples by language:
  - [C#](https://github.com/MetricsHub/AzureStoreRP)
  - [Python Flask](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/samples/python-flask)
  - [Node.js](https://github.com/auth0/node-azure-store)


