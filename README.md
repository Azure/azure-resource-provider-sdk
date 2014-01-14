# Windows Azure Store SDK

**[LOOKING FOR API DOCS?](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs)**

This SDK is intended for a technical audience (developers or PMs) and provides all the information needed to launch a product or service inside the [Windows Azure Store](http://www.windowsazure.com/en-us/store/overview/).  

![overview](https://raw.github.com/WindowsAzure/azure-resource-provider-sdk/master/docs/images/azure-store1.png)  

This SDK includes:
- [Technical Documentation and Samples](https://github.com/WindowsAzure/azure-resource-provider-sdk/blob/master/README.md#technical-documentation-and-samples) for building a Resource Provider (web service) for the Windows Azure Store.
- An [Onboarding Guide](https://github.com/WindowsAzure/azure-resource-provider-sdk/blob/master/README.md#onboarding-guide) to walk you through all the steps required to get an Add-on into the Windows Azure Store; from creating your Seller Account with Microsoft, to releasing our Add-on into Production.
- An [FAQ](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/faq.md) to help answer your questions.

**Please note:** the Windows Azure Store is currently in Preview and this is a pre-release SDK and constantly evolving based on customer feedback.


## Onboarding Guide

**GET STARTED HERE**

The following steps outline the entire cycle of developing, launching and maintaining an Add-on in the Windows Azure Store.  These steps represent a mix of development and project management work.

**Step 1: Submit Microsoft Seller Application.**  You must be an approved seller in order to publish and Add-on in the Windows Azure Store and receive payout.  Note that if you have already released an app you may already be an approved seller.  You only need one approved seller account to sell apps and services in Microsoft Marketplaces.  Read the [Publisher Portal Guide](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/publisher-portal.md) to learn how to start the Seller Application process.  This step must be completed before Step 5.

**Step 2: Create Your Publisher Portal Account and Define Your Add-on.**  The Publisher Portal is how you will manage the details of your Add-on, including marketing copy, pricing and endpoints for your Resource Provider.  Read the [Publisher Portal Guide](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/publisher-portal.md) to get started. This step can be done in parallel with Steps 1, 3 and 4.

**Step 3: Build and Test Your Resource Provider.**  A Resource Provider is the web service that allows users to purchase your Add-on from the Windows Azure Store and manage it from within the Windows Azure Management Portal.  Read the [Resource Provider API Guide](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/README.md) to get started building your Resource Provider.  This step can be done in parallel with Steps 1, 2 and 3.

**Step 4: Publish Your Add-on to Preview.**  In order to test how your Add-on will look and work in the Windows Azure Store, we have a preview/test enviroment that using accounts with test billing info in order to fully test your Add-on.

**Step 5: Publish Your Add-on to Production.** Once your Add-on is tested and working in Preview, you will use the Publishing Portal to publish your Add-on to production.  This will initiate a final review process by Microsoft Store admins.  When your Add-on is approved it will be released to the live Windows Azure Store.

**Step 6: Schedule Co-marketing for Your Add-on.** Use some Windows Azure marketing muscle to grow awareness of your Add-on.  Read here (coming soon) about co-marketing opportunities.  This step can be done at anytime.

**Step 7: Fine-tune Your Add-on.**  Unless you got it completely right the first time, you will want to use the Publisher Portal to adjust pricing and tiers, descriptions and make some promo codes.  Read here (coming soon) about how to make changes to your Add-on.  This step can be done at anytime.

##Technical Documentation and Samples

**Please note:** the Windows Azure Store is currently in Preview and we are currently working on a new .NET SDK that will make it easy to quickly standup a Resource Provider for your Add-on.  We expect to release this new SDK by late February.

- [API reference](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs)
- Code samples by language:
  - [C#](https://github.com/MetricsHub/AzureStoreRP)
  - [Python Flask](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/samples/python-flask)
  - [Node.js](https://github.com/auth0/node-azure-store)


