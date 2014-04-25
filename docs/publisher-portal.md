# Publisher Portal Guide
The [Publisher Portal](http://publish.windowsazure.com) is the tool you will use define and manage your Add-on. Think of it as the CMS for you Add-on.  Using the Publisher Portal you will:

- Tell us about your company, e.g. who do we contact for customer support, and where do we send electronic payments.
- Define your Add-on, including price tiers and web service endpoints.
- Submit your Add-on for testing and approval.

You will use the Publisher Portal to perform each of following tasks below.  These tasks are ordered in the sequence you will perform them.

- [Provide Your Company Information](#provide-company-information)
- [Submit Your Seller Application](#submit-your-seller-application)
- [Define Your Add-on](#define-your-add-on)
- [Publish Your Add-on To Preview](#publish-your-add-on-to-preview)
- [Publish Your Add-on To Production](#publish-your-add-on-to-production)

##Provide Company Information

Log into the [Publisher Portal](http://publish.windowsazure.com) with your Microsoft account.  If you do not have one you will be directed to create one [here](http://go.microsoft.com/fwlink/p/?LinkID=238657).

    > **Note:** When creating your Publisher Portal login make sure to use an account that is shared among members of your team.  For example:  AzStore-Admin@contoso.com vs. joesmith@contoso.com .


When you login for the first time, you will be required to set a _Publisher Namespace_.  This is a unique identifier for your company, and it is also used when [Azure Management API](http://msdn.microsoft.com/library/azure/ee460799.aspx) users call your Resource Provider directly. You should use a concise string representing your company. For example, if your company is called Clouditrace and sells a monitoring service, you should enter "clouditrace" and not "monitoring" because the later is too specific.

![overview](https://raw.github.com/Azure/azure-resource-provider-sdk/master/docs/images/publisher-portal-namespace.PNG)

##Submit Your Seller Application
After signing up in the Publisher Portal, click on the _Publishers_ tab.  Your Publisher Namespace will be displayed along with a status of "Needs attention".

![overview](https://raw.github.com/Azure/azure-resource-provider-sdk/master/docs/images/publisher-portal-seller-dashboard.PNG)

Click the pop-out icon to launch the Seller Dashboard.  All Azure Store partners are **required** to submit an application in order to be approved to offer products and services in the Azure Store.  The Seller Dashboard is where you fill in your company details, submit an application to become a seller in Microsoft marketplaces and manage your payout information.  We strongly encourage partners to start this process early in order to prevent delays in onboarding.

![overview](https://raw.github.com/Azure/azure-resource-provider-sdk/master/docs/images/seller-dashboard-site.PNG)

For help with the Microsoft Seller Dashboard please see this [FAQ](http://msdn.microsoft.com/en-us/library/jj552463.aspx).

##Define Your Add-on
Now that you have created a Publisher account and submitted your Seller application, you are ready to create your first _Add-on_.  An _Add-on_ is product or service listing in the Azure Store.  Within the Publisher Portal, click _New_ at the bottom, then _App Service_, _Azure Store_ and _Quick Create_.  Enter the Title of your Add-on and then click _Create New Azure Store Offer_.

![overview](https://raw.github.com/Azure/azure-resource-provider-sdk/master/docs/images/publisher-portal-create-offer.PNG)

Once your new _Add-on_ is created you will be shown the dashboard for your _Add-on_, along with details on next steps.

![overview](https://raw.github.com/Azure/azure-resource-provider-sdk/master/docs/images/publisher-portal-offer-next-steps.PNG)

Continue building your new Add-on by following the directions in the Publisher Portal.  You will need to define your Add-on _Service Plans_, Marketing copy, Pricing, Support links, Resource Provider endpoints and Data Centers.


_Service Plans_ are the different price and feature tiers within an _Add-on_.  To create a _Service Plan_, select the _App Services_ tab, select an _Offer_, and select _Plans_ in the top nav.  Then select _Add Plan_ at the bottom to launch _Add a New Plan_ dialog.  Use the tool tips to learn more about configuring _Service Plans_.

![overview](https://raw.github.com/Azure/azure-resource-provider-sdk/master/docs/images/publisher-portal-add-plan.PNG)

**Notes on Service Plans:**

* Free trial plans are not currently supported. **Free plans must be always free.**
* **Plan Identifier** is the display name of your Add-on e.g. Free, Nano, Micro, Mega. Free plans are required to be called Free. **Plan names should not exceed 50 characters.**

##Publish Your Add-on To Preview
Once you have filled out all the information for you Add-on in the Publisher Portal AND developed your Resource Provider, you can Publish your Add-on to Preview in order to test the functionality of your Add-on in a test version of the Azure Store. Select your Add-on in the Publisher Portal and go to the _Publish_ section and select _Preview_ at the bottom.  This will publish your Add-on to our staging environment for further testing.  For access to the Azure Store test enviroment, contact the Microsoft PM helping you onboard into the Azure Store.

![overview](https://raw.github.com/Azure/azure-resource-provider-sdk/master/docs/images/publisher-portal-publish.png)


##Publish Your Add-on To Production
Once you have tested your Add-on in the test environment, resolved all issues and are ready for your Add-on to be availble in the live Azure Store, you will Publish to Production.  Select your Add-on in the Publisher Portal and go to the _Publish_ section and select _Publish_ at the bottom.  **This action does not automatically publish your Add-on to the live Store**, but rather it puts your Add-on into a queue to be approved for release in the live Store.  After you select the _Publish_ action, notify your Microsoft PM that your Add-on is published and waiting approval.  Approvals take 1-2 days.


