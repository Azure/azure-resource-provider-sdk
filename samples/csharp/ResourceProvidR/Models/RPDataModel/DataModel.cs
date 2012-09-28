using Microsoft.WindowsAzure.CloudServiceManagement;
using Microsoft.WindowsAzure.CloudServiceManagement.ResourceProviderCommunication;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Web;
using System.Web.Http;

namespace ResourceProvidR.Models.RPDataModel
{
    internal class CloudService
    {
        public string Name { get; set; }
        public int IncarnationId { get; set; }
        public string GeoLocation { get; set; }

        public List<ResourceOutput> Resources { get; private set; }

        public CloudService()
        {
            IncarnationId = 0;
            GeoLocation = "";
            Resources = new List<ResourceOutput>();
        }
    }

    internal class Subscription
    {
        public Guid Id { get; set; }
        public List<CloudService> CloudServices { get; private set; }

        public Subscription()
        {
            CloudServices = new List<CloudService>();
        }
    }

    public static class DataModel
    {
        private static object theMassiveLock = new object();
        private static Dictionary<Guid, Subscription> allSubscriptions = new Dictionary<Guid, Subscription>();

        public static void DeleteCloudService(Guid subscriptionId, string cloudServiceName)
        {
            lock (theMassiveLock)
            {
                Subscription subscription;
                if (!allSubscriptions.TryGetValue(subscriptionId, out subscription))
                {
                    throw new HttpResponseException(HttpStatusCode.NotFound);
                }

                CloudService theMatchingCloudService = subscription.CloudServices.SingleOrDefault<CloudService>(cs => String.CompareOrdinal(cs.Name, cloudServiceName) == 0);

                if (theMatchingCloudService == null)
                {
                    throw new HttpResponseException(HttpStatusCode.NotFound);
                }

                subscription.CloudServices.Remove(theMatchingCloudService);
            }
        }

        public static ResourceOutput InsertOrUpdateResource(Guid subscriptionId, string cloudServiceName, string resourceType, string resourceName, ResourceInput resource)
        {
            ResourceOutput output;

            lock (theMassiveLock)
            {
                Subscription subscription;
                if (!allSubscriptions.TryGetValue(subscriptionId, out subscription))
                {
                    subscription = new Subscription() { Id = subscriptionId };
                    allSubscriptions[subscriptionId] = subscription;
                }

                CloudService theMatchingCloudService = subscription.CloudServices.SingleOrDefault<CloudService>(cs => String.CompareOrdinal(cs.Name, cloudServiceName) == 0);

                if (theMatchingCloudService == null)
                {
                    theMatchingCloudService = new CloudService() { Name = cloudServiceName };
                    subscription.CloudServices.Add(theMatchingCloudService);
                }

                // Victor says "do not increment incarnation ids"
                //theMatchingCloudService.IncarnationId++;

                ResourceOutput theMatchingResource = theMatchingCloudService.Resources.FirstOrDefault(r => String.Compare(r.Name, resourceName) == 0);

                if (theMatchingResource != null)
                {
                    if (theMatchingResource.IncarnationId != resource.IncarnationId)
                    {
                        theMatchingResource.CloudServiceSettings = resource.CloudServiceSettings;
                        theMatchingResource.IncarnationId = resource.IncarnationId;
                        theMatchingResource.IntrinsicSettings = resource.IntrinsicSettings;
                        theMatchingResource.Name = resourceName;
                        theMatchingResource.OperationStatus = new OperationStatus()
                        {
                            Error = new ErrorData() { HttpCode = 200, Message="OK" }, 
                            Result = OperationResult.Succeeded
                        };
                        theMatchingResource.OutputItems = new OutputItemList(new List<OutputItem>() {
                            new OutputItem() { Key="ProvidR-Output-1", Value = DateTime.Now.ToShortDateString() },
                            new OutputItem() { Key="ProvidR-Output-2", Value = Environment.MachineName }
                        });
                        theMatchingResource.Plan = resource.Plan;
                        theMatchingResource.SchemaVersion = resource.SchemaVersion;
                        theMatchingResource.State = ResourceState.Started;
                        theMatchingResource.SubState = "";
                        theMatchingResource.Type = resource.Type;
                    }

                    output = theMatchingResource;
                }
                else
                {
                    output = new ResourceOutput()
                    {
                        CloudServiceSettings = resource.CloudServiceSettings,
                        IncarnationId = resource.IncarnationId,
                        IntrinsicSettings = resource.IntrinsicSettings,
                        Name = resourceName,
                        OperationStatus = new OperationStatus()
                        {
                            Error = new ErrorData() { HttpCode = 200, Message="OK" }, 
                            Result = OperationResult.Succeeded
                        },
                        OutputItems = new OutputItemList(new List<OutputItem>() {
                            new OutputItem() { Key="ProvidR-Output-1", Value = DateTime.Now.ToShortDateString() },
                            new OutputItem() { Key="ProvidR-Output-2", Value = Environment.MachineName }
                        }),
                        Plan = resource.Plan,
                        SchemaVersion = resource.SchemaVersion,
                        State = ResourceState.Started,
                        SubState = "",
                        Type = resource.Type
                    };

                    theMatchingCloudService.Resources.Add(output);
                }
            }

            return output;
        }

        public static CloudServiceOutput GetCloudServiceBySubscriptionIdAndName(Guid subscriptionId, string cloudServiceName)
        {
            lock (theMassiveLock)
            {
                Subscription subscription;
                if (!allSubscriptions.TryGetValue(subscriptionId, out subscription))
                {
                    throw new HttpResponseException(HttpStatusCode.NotFound);
                }

                CloudService theMatchingCloudService = subscription.CloudServices.SingleOrDefault<CloudService>(cs => String.CompareOrdinal(cs.Name, cloudServiceName) == 0);

                if (theMatchingCloudService == null)
                {
                    throw new HttpResponseException(HttpStatusCode.NotFound);
                }

                CloudServiceOutput cloudServiceOutput = new CloudServiceOutput()
                {
                    GeoLocation = theMatchingCloudService.Resources.Count > 0 ? theMatchingCloudService.Resources[0].CloudServiceSettings.GeoLocation : String.Empty,
                    IncarnationId = theMatchingCloudService.IncarnationId,
                    Resources = new ResourceOutputCollection(theMatchingCloudService.Resources)
                };

                return cloudServiceOutput;
            }
        }

        public static CloudServiceOutputCollection GetCloudServicesForSubscription(Guid subscriptionId)
        {
            // TODO
            return null;
        }

        public static void DeleteResource(Guid subscriptionId, string cloudServiceName, string resourceName)
        {
            lock (theMassiveLock)
            {
                Subscription subscription;
                if (!allSubscriptions.TryGetValue(subscriptionId, out subscription))
                {
                    throw new HttpResponseException(HttpStatusCode.NotFound);
                }

                CloudService theMatchingCloudService = subscription.CloudServices.SingleOrDefault<CloudService>(cs => String.CompareOrdinal(cs.Name, cloudServiceName) == 0);

                if (theMatchingCloudService == null)
                {
                    throw new HttpResponseException(HttpStatusCode.NotFound);
                }

                ResourceOutput theMatchingResource = theMatchingCloudService.Resources.FirstOrDefault(r => String.Compare(r.Name, resourceName) == 0);

                if (theMatchingResource != null)
                {
                    // Do not increment incarnation ids
                    //theMatchingCloudService.IncarnationId++;
                    theMatchingCloudService.Resources.Remove(theMatchingResource);
                }
                else
                {
                    throw new HttpResponseException(HttpStatusCode.NotFound);
                }
            }
        }

        public static ResourceOutput GetResource(Guid subscriptionId, string cloudServiceName, string resourceName)
        {
            lock (theMassiveLock)
            {
                Subscription subscription;
                if (!allSubscriptions.TryGetValue(subscriptionId, out subscription))
                {
                    throw new HttpResponseException(HttpStatusCode.NotFound);
                }

                CloudService theMatchingCloudService = subscription.CloudServices.SingleOrDefault<CloudService>(cs => String.CompareOrdinal(cs.Name, cloudServiceName) == 0);

                if (theMatchingCloudService == null)
                {
                    throw new HttpResponseException(HttpStatusCode.NotFound);
                }

                ResourceOutput theMatchingResource = theMatchingCloudService.Resources.FirstOrDefault(r => String.Compare(r.Name, resourceName) == 0);

                if (theMatchingResource != null)
                {
                    return theMatchingResource;
                }
                else
                {
                    throw new HttpResponseException(HttpStatusCode.NotFound);
                }
            }
        }
    }
}