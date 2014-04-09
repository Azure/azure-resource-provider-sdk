# Azure Store Partner FAQ

## General questions about selling in the Azure Store
- [What countries is the Azure Store available to Sell From?](#what-countries-is-the-azure-store-available-to-sell-from)
- [What countries is the Azure Store available to Sell To?](#what-countries-is-the-azure-store-available-to-sell-to)

## Questions related to the Publisher Portal
- [How do I upgrade to the new Publisher Portal?](#how-do-i-upgrade-to-the-new-publisher-portal)
- [Why does my Publisher account still say "Needs Attention"?](#why-does-my-publisher-account-still-say-needs-attention)
- [How do I update my Add-on logos displayed on the Azure website?](#how-do-i-update-my-add-on-logos-displayed-on-the-azure-website)
- [Do I have to publish updates to promo codes?](#do-i-have-to-publish-updates-to-promo-codes)
- [What happens to existing customers if I change the price of a Plan?](#what-happens-to-existing-customers-if-i-change-the-price-of-a-plan)

## Questions related to developing a Resource Provider
- [Which characters need to be supported for resource names?](#which-characters-need-to-be-supported-for-resource-names)

### What countries is the Azure Store available to Sell From?
During the preview, the Azure Store is available only in the United States.

### What countries is the Azure Store available to Sell To?
Windows Azure Store is currently available to consumers in the following countries:

Algeria - Argentina - Australia - Austria - Bahrain - Belarus - Belgium - Brazil - Bulgaria - Canada - Chile - Colombia - Costa Rica - Czech Republic - Denmark - Dominican Republic - Ecuador - Egypt - El Salvador - Estonia - Finland - France - Germany - Great Britain (United Kingdom) - Greece - Guatemala - HongKong - Hungary - Indonesia - Ireland - Israel - Italy - Japan - Jordan - Kazakhstan - Kenya - Kuwait - Latvia - Lithuania - Luxembourg - Macedonia - Malaysia - Malta - Mexico - 
Montenegro - Morocco - Netherlands - New Zealand - Nigeria - Oman - Pakistan - Panama - Paraguay - Peru - Philippines - Poland - Portugal - Qatar - Romania - Russia - Saudi Arabia - Serbia - Singapore - Slovakia - Slovenia - South Africa - South Korea - Spain - Sri Lanka - Sweden - Switzerland - Thailand - Trinidad and Tobago - Tunisia - Turkey - Ukraine - United Arab Emirates - United States - Uruguay - Venezuela

### How do I upgrade to the new Publisher Portal?
If you launched your Add-on into the Azure Store before October 2013, you were on-boarded using an older version of the Azure Publisher Portal. Our new Publisher Portal supports additional options to configure your Add-on and associated Plans. We have automatically migrated all data from the old portal to the new portal. To get access to your existing data all you need to do is log-in with the same Live ID as the one that you used in the old portal.

To complete migration to the new Publisher Portal, you will need to complete two steps:

#### 1) Update your company profile and tax status in the Seller Dashboard.

The new portal uses the centralized Microsoft seller registration dashboard to confirm who you are as a publisher. If you do not yet have a seller profile with Microsoft (shared across Windows, Windows Phone and Azure Store) you will need to visit http://sellerdashboard.microsoft.com as part of the publishing process in the new portal to set up your Tax information and Payout information.

#### 2) Publish your Add-on to Preview and Production.

All data regarding your Add-on has been migrated, however you will need to re-publish your Add-on to the Preview and Production environments.  This step will complete the connection between the new Publisher Portal and your Add-ons in Preview and Production.  To Publish to Preview and Production, go to your Add-on, select the "Publish" tab, then using the bottom toolbar, complete the "Preview" action and once it has completed, the "Publish" action.

The new Publisher Portal is located at http://publish.windowsazure.com.  Follow the [Publisher Portal Guide](https://github.com/WindowsAzure/azure-resource-provider-sdk/tree/master/docs/publisher-portal.md) to get started with the new Publisher Portal.

### Why does my Publisher account still say "Needs Attention"?

In order to release your Add-on into the Azure Store you will need to be an approved Seller.  To apply for approval, you need to submit an application with the Seller Dashboard, which is the first step in setting up your Publisher Portal account.  Until you are approved as a Seller, the Publisher Portal will display the warning "Needs attention" next to your Publisher name.  To check the status of your account, click the "Update Status" button in the bottom toolbar.  If you have been approved, this warning will go away.  If you have not been approved, you will still see the warning, and should contact your Azure Store PM for status.

![overview](https://raw.github.com/WindowsAzure/azure-resource-provider-sdk/master/docs/images/publisher-portal-update-status.png)


### How do I update my Add-on logos displayed on the Azure website? 
As of December 2013 we support higher resolution Add-on logos on Azure Store pages.  To update your Add-on logos you will need to log into the [Publisher Portal](http://publish.windowsazure.com).  If you are not using the new Publisher Portal you will need to upgrade by following the steps in "How do I upgrade to the new Publisher Portal?".

1. Log into the [Publisher Portal](http://publish.windowsazure.com).
2. Select the vertical tab "App Services"
3. Select your Add-on
4. Select the horizontal tab “Marketing”
5. Select “English” or other language where relevant
6. Upload your new logos

![overview](https://raw.github.com/WindowsAzure/azure-resource-provider-sdk/master/docs/images/publisher-portal-marketing-details.png)

### Do I have to publish updates to promo codes?
If you want to make a change to an existing promo code, simply make the edits and save.  Those changes will take effect immediately without the need to re-publish to Preview or Production.

### What happens to existing customers if I change the price of a Plan?
If you change the price of an existing Plan, customers that are already subscribed to that Plan are not effected by the price change.  Those existing customers will continue on the Plan at the the price/rate they originally purchased.

### What happens if I delete a Plan that has customers?
Deleting a Plan in the Publisher Portal will remove the Plan from the Azure Store.  The Azure Store backend will no longer support selling of this Plan, but existing customers won’t be effected.

### Which characters need to be supported for resource names?

The Azure Store allows users to use letters, numbers, periods, hyphens and underscores when creating resource names.  Your service will need to accept these characters when provisioning resources.  If your service is not able to accept any of these allowed characters, then one option is to: reject the resource creation and return a user friendly error message that identifies the rejected character(s), and communicates allowed characters.
