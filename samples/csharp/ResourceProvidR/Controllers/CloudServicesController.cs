/*
* Copyright 2011 Microsoft Corporation
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*   http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*
*/

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