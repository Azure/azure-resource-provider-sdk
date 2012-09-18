using System;
using System.Net;
using System.Web.Http;
using Microsoft.WindowsAzure.CloudServiceManagement.ResourceProviderCommunication;
using ResourceProvidR.Models;

namespace ResourceProvidR.Controllers
{
    public class ResourcesController : ApiController
    {
        //
        // GET /subscriptions/{subscriptionId}/cloudservices/{cloudServiceName}/resources/{resourceName}
        //
        [HttpGet]
        public ResourceOutput GetResource(string subscriptionId, string cloudServiceName, /*string resourceType,*/ string resourceName)
        {
            if (String.IsNullOrEmpty(cloudServiceName) /*|| String.IsNullOrEmpty(resourceType)*/ || String.IsNullOrEmpty(resourceName))
            {
                throw new HttpResponseException(HttpStatusCode.BadRequest);
            }

            return DataModel.GetResource(subscriptionId, cloudServiceName, resourceName);
        }

        //
        // PUT /subscriptions/{subscriptionId}/cloudservices/{cloudServiceName}/resources/{resourceName}
        //
        [HttpPut]
        public ResourceOutput ProvisionOrUpdateResource(string subscriptionId, string cloudServiceName, /*string resourceType,*/ string resourceName, ResourceInput resource)
        {
            if (String.IsNullOrEmpty(cloudServiceName) /*|| String.IsNullOrEmpty(resourceType)*/ || String.IsNullOrEmpty(resourceName) || (resource == null))
            {
                throw new HttpResponseException(HttpStatusCode.BadRequest);
            }

            return DataModel.ProvisionOrUpdateResource(subscriptionId, cloudServiceName, null, /*resourceType,*/ resourceName, resource);
        }

        //
        // DELETE /subscriptions/{subscriptionId}/cloudservices/{cloudServiceName}/resources/{resourceName}
        //
        [HttpDelete]
        public void DeleteResource(string subscriptionId, string cloudServiceName, /*string resourceType,*/ string resourceName)
        {
            if (String.IsNullOrEmpty(cloudServiceName) /*|| String.IsNullOrEmpty(resourceType)*/ || String.IsNullOrEmpty(resourceName))
            {
                throw new HttpResponseException(HttpStatusCode.BadRequest);
            }

            DataModel.DeleteResource(subscriptionId, cloudServiceName, resourceName);
        }

        //
        // GET /subscriptions/{subscriptionId}/cloudservices/{cloudServiceName}/resources/{resourceType}/{resourceName}/GenerateSSOToken
        //
        //[HttpGet]
        //public void GenerateSSOToken(string subscriptionId, string cloudServiceName, /*string resourceType,*/ string resourceName)
        //{
        //}
    }
}
