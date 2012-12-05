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

using System.Web.Http;

namespace ResourceProvidR
{
    public static class WebApiConfig
    {
        public static void Register(HttpConfiguration config)
        {
            // -------- Subscription Notifications --------
            // POST /events
            config.Routes.MapHttpRoute(
                name: "Events",
                routeTemplate: "{subscriptionId}/events",
                defaults: new { controller = "Events", action = "HandleSubscriptionNotifications" }
            );

            // -------- Cloud Services Management --------

            // Cloud Service level resource management
            // GET /subscriptions/{subscriptionId}/cloudservices/{cloudServiceName}
            // DELETE /subscriptions/{subscriptionId}/cloudservices/{cloudServiceName}
            config.Routes.MapHttpRoute(
               name: "CloudService-Management",
               routeTemplate: "subscriptions/{subscriptionId}/cloudservices/{cloudServiceName}",
               defaults: new {
                   controller = "CloudServices"
               }
           );

           // -------- Resource Management --------

            // GET /subscriptions/{subscriptionId}/cloudservices/{cloudServiceName}/resources/{resourceType}/{resourceName}
            // PUT /subscriptions/{subscriptionId}/cloudservices/{cloudServiceName}/resources/{resourceType}/{resourceName}
            // DELETE subscriptions/{subscriptionId}/cloudservices/{cloudServiceName}/resources/{resourceType}/{resourceName}
           config.Routes.MapHttpRoute(
               name: "Resource-Management",
               routeTemplate: "subscriptions/{subscriptionId}/cloudservices/{cloudServiceName}/resources/{resourceType}/{resourceName}",
               defaults: new
               {
                   controller = "Resources"
               }
           );

           // -------- Single Sign On --------

           // GET subscriptions/{subscriptionId}/cloudservices/{cloudServiceName}/resources/{resourceType}/{resourceName}/GenerateSSOToken
           config.Routes.MapHttpRoute(
               name: "Resource-Management-SingleSignOn",
               routeTemplate: "subscriptions/{subscriptionId}/cloudservices/{cloudServiceName}/resources/{resourceType}/{resourceName}/SsoToken",
               defaults: new
               {
                   controller = "Resources",
                   action = "SsoToken"
               }
           );
        }
    }
}