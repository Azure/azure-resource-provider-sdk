Publisher Portal Guide
===
The [Publisher Portal](http://publish.marketplace.windowsazure.com) is the web site where you can create and manage your offering. This process involves several steps:

1. Login with a Microsoft account. If you do not have a Microsoft account, [get one](http://go.microsoft.com/fwlink/p/?LinkID=238657).
2. Tell us about your company e.g. who do we contact for customer support, and where do we send electronic payments.
3. Create an offering, including registering your RP
4. Submit the offering for testing and approval

Step 1: Provide company information
---
When you login for the first time, you will be required to provide information about your company. There are two important items to pay attention to:

* **Company Identifier / Resource Provider Namespace**: Pay particular attention to this value. This is a unique identifier of your company, and it is also used when [Windows Azure Management API](http://msdn.microsoft.com/en-us/library/windowsazure/ee460799.aspx) users call your Resource Provider directly. You should use a concise string representing your company. For example, if your company is called Contoso and sells a monitoring service, you should enter "contoso" and not "monitoring" because the latter is too specific.

* **Tax Profile Type ** If you are a business, choose _Company_. Otherwise, choose _Individual_.

![overview](https://raw.github.com/WindowsAzure/azure-resource-provider-sdk/master/docs/images/publishing-portal-10.png)

Step 2: Create an offering
---
You are ready to create your first offering. Click the _Publish_ tab:

![overview](https://raw.github.com/WindowsAzure/azure-resource-provider-sdk/master/docs/images/publishing-portal-09.png)

and click _Add App Service_:

![overview](https://raw.github.com/WindowsAzure/azure-resource-provider-sdk/master/docs/images/publishing-portal-08.png)

Paste in your [manifest](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/manifest.md):

![overview](https://raw.github.com/WindowsAzure/azure-resource-provider-sdk/master/docs/images/publishing-portal-07.png)

Click _Contacts_. Information you enter on this page will be shown to users in various places to help them get support:

![overview](https://raw.github.com/WindowsAzure/azure-resource-provider-sdk/master/docs/images/publishing-portal-06.png)

Click _Details_, and provide details about your offering:

![overview](https://raw.github.com/WindowsAzure/azure-resource-provider-sdk/master/docs/images/publishing-portal-05.png)

* **Resource Type Display Name** is the name of the offering as it will appear to users in our catalog. For example, it could be "Clouditrace" or "ContosoDB".
* **Short Description** is a brief description of your offering. It cannot exceed **500 characters**.
* **Long Description** is a long description of your offering. It is **not currently used**.
* **Resource Type** is your RP's `ResourceType` and is passed to you in [Create Resource](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/api-resource-create.md) requests in the `Resource/Type` node.
* **Links** You should add as many links in the Links section as possible. We require that you link to an API reference, a quick-start guide, and sample code.

![overview](https://raw.github.com/WindowsAzure/azure-resource-provider-sdk/master/docs/images/publishing-portal-04.png)

* **Regions** If you service is deployed in a Windows Azure datacenter, you are required to specify what datacenters are available. Otherwise, leave this field blank.
* **Logos** You are required to provide three logos, 45x45, 100x100 and 215x215. Please refer to the [brand guide](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/brand-guide.md) for logo requirements.

Click _Plans_ to specify free and paid plans for your offering:

![overview](https://raw.github.com/WindowsAzure/azure-resource-provider-sdk/master/docs/images/publishing-portal-03.png)

* **Name** is the display name of your offering e.g. Free, Nano, Micro, Mega. Free plans are required to be called Free.
* **Unique Identifier** is the ID of the plan. It will be passed to you in the [Create Resource](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/api-resource-create.md) and [Upgrade Resource](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/api-resource-upgrade.md) requests in the `Resource/Type` node.
* **Description** is a brief description of the plan. We recommend keeping this field brief, no more than three plain-text sentences.
* **Retail Price** is the price of your offering in USD. Regardless of what country your offering is available in, you always specify the price in [USD](http://en.wikipedia.org/wiki/United_States_dollar). Windows Azure will automatically price the offering in the local currency if it's available.
* **Markets** are the countries and regions your offering is available. We recommend choosing _All markets_ to make your service available wherever Windows Azure is available.

![overview](https://raw.github.com/WindowsAzure/azure-resource-provider-sdk/master/docs/images/publishing-portal-02.png)

* **Terms of Use** are required. **You cannot enter a URL for Terms of Use**. Please provide plain-text terms without any markup. A privacy URL is also required.

Step 3: Submit your offering
---

![overview](https://raw.github.com/WindowsAzure/azure-resource-provider-sdk/master/docs/images/publishing-portal-01.png)

Click _Status/Review_ and if your offering passes validation checks, click _Submit_.

Next Steps
---

* Microsoft will work with you to test your offering in staging
* When your offering passes tests, we will enable it in production
* You will come back to the _Status/Review_ page and click _Publish_ (not avaialble while an offer is in review) to make the offering available to Windows Azure users.