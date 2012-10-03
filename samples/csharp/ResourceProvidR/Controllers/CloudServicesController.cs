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
        public CloudServiceOutput DeleteCloudService(string subscriptionId, string cloudServiceName)
        {
            if (String.IsNullOrEmpty(cloudServiceName))
            {
                throw new HttpResponseException(HttpStatusCode.NotFound);
            }

            return DataModel.DeleteCloudService(subscriptionId, cloudServiceName);
        }
    }
}