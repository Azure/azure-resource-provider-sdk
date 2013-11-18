Publisher Portal Guide
===
The [Publisher Portal](http://publish.windowsazure.com) in a web site where you can create and manage your offering. Using the Publishing Portal you will:

1. Tell us about your company, e.g. who do we contact for customer support, and where do we send electronic payments.
2. Create your offering, including registering your Resource Provider.
3. Submit your offering for testing and approval.

Step 1: Provide company information
---
Log into the [Publisher Portal](http://publish.windowsazure.com) with your Microsoft account.  If you do not have one you will be directed to create one [here](http://go.microsoft.com/fwlink/p/?LinkID=238657).

When you login for the first time, you will be required to set a _Publisher Namespace_.  This is a unique identifier for your company, and it is also used when [Windows Azure Management API](http://msdn.microsoft.com/en-us/library/windowsazure/ee460799.aspx) users call your Resource Provider directly. You should use a concise string representing your company. For example, if your company is called Clouditrace and sells a monitoring service, you should enter "clouditrace" and not "monitoring" because the later is too specific.

![overview](https://raw.github.com/WindowsAzure/azure-resource-provider-sdk/master/docs/images/publisher-portal-namespace.png)

Step 2: Submit your seller application
---
After signing up in the Publishing Portal, click on the _Publishers_ tab.  Your Publisher Namespace will be displayed along with a status of "Needs attention".  

![overview](https://raw.github.com/WindowsAzure/azure-resource-provider-sdk/master/docs/images/publisher-portal-seller-dashboard.png)

Click the pop-out icon to launch the Seller Dashboard.  All Azure Store partners are **required** to submit an application in order to be approved to offer products and services in the Azure Store.  The Seller Dashboard is where you fill in your company details, submit an application to become a seller in Microsoft marketplaces and manage your payout information.  We strongly encourage partners to start this process early in order to prevent delays in onboarding. 

![overview](https://raw.github.com/WindowsAzure/azure-resource-provider-sdk/master/docs/images/seller-dashboard-site.png)

For help with the Microsoft Seller Dashboard please see this [FAQ](http://msdn.microsoft.com/en-us/library/jj552463.aspx).

Step 3: Create your offer
---
Now that you have created a Publisher account and submitted your Seller application, you are ready to create your first _Offer_.  An _Offer_ is product or service listing in the Azure Store.  Within the Publisher Portal, click _New_ at the bottom, then _App Service_, _Azure Store_ and _Quick Create_.  Enter the Title of your offer and then click _Create New Azure Store Offer_.

![overview](https://raw.github.com/WindowsAzure/azure-resource-provider-sdk/master/docs/images/publisher-portal-create-offer.png)

Once you new _Offer_ is created you will be shown the dashboard for your _Offer_, along with details on next steps.

![overview](https://raw.github.com/WindowsAzure/azure-resource-provider-sdk/master/docs/images/publisher-portal-offer-next-steps.png)

Step 4: Add one or more plans in your offer
---
_Plans_ are the different price and feature tiers within an _Offer_.  To create a _Plan_, select the _App Services_ tab, select an _Offer_, and select _Plans_ in the top nav.  Then select _Add Plan_ at the bottom to launch _Add a New Plan_ dialog.  Use the tool tips to learn more about configuring _Plans_.

![overview](https://raw.github.com/WindowsAzure/azure-resource-provider-sdk/master/docs/images/publisher-portal-add-plan.PNG)

**Notes on Plans:** 

* Free trial plans are not currently supported. **Free plans must be always free.**
* **Plan Identifier** is the display name of your offering e.g. Free, Nano, Micro, Mega. Free plans are required to be called Free. **Plan names should not exceed 50 characters.**

Step 5: Configure, build and test your offering
---
Continue completing the steps listed in the Publisher Portal, eventually filling out and configuring each section of your offer (Plans, Marketing, Pricing, Support, Resource Provider and Data Centers).  Once you have implemented your Resource Provided you can go to the _Publish_ section, and select _Preview_ at the bottom, which will publish your Offer to our staging environment for further testing.

Next Steps
---

* Microsoft will work with you to test your offer in staging
* When your offer passes tests, we will ask you to _Publish_ your offer.
* After you select _Publish_ your offer will not be live, but will be submitted for final review by Microsoft.  Once final review is completed, we can publish your offer to production.