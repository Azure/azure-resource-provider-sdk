using System;
using System.Net;
using System.Web.Http;
using Microsoft.WindowsAzure.CloudServiceManagement.ResourceProviderCommunication;
using ResourceProvidR.Models;

namespace ResourceProvidR.Controllers
{
    public class CloudServicesController : ApiController
    {
        //
        // GET /subscriptions/{subscriptionId}/cloudservices
        //
        [HttpGet]
        public CloudServiceOutputCollection GetAllCloudServices(string subscriptionId)
        {
            // This is not currently being called by Windows Azure
            return DataModel.GetAllCloudServicesForSubscription(subscriptionId);
        }

        //
        // GET /subscriptions/{subscriptionId}/cloudservices/{cloudServiceName}
        //
        [HttpGet]
        public CloudServiceOutput GetAllResourcesInCloudService(string subscriptionId, string cloudServiceName)
        {
            if (String.IsNullOrEmpty(cloudServiceName))
            {
                throw new HttpResponseException(HttpStatusCode.BadRequest);
            }

            return DataModel.GetCloudServiceBySubscriptionIdAndName(subscriptionId, cloudServiceName);
        }

        //
        // DELETE /subscriptions/{subscriptionId}/cloudservices/{cloudServiceName}
        //
        [HttpDelete]
        public void DeleteCloudService(string subscriptionId, string cloudServiceName)
        {
            if (String.IsNullOrEmpty(cloudServiceName))
            {
                throw new HttpResponseException(HttpStatusCode.NotFound);
            }

            DataModel.DeleteCloudService(subscriptionId, cloudServiceName);
        }
    }
}