using System;
using System.Collections.Generic;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.ServiceModel.Web;
using System.Xml;

namespace Microsoft.WindowsAzure.CloudServiceManagement.ResourceProviderCommunication
{
    /// <summary>
    /// Name of well known Output Values displayed in the Windows Azure Management Portal.
    /// </summary>
    public static class WellKnownOutputValues
    {
        public const string ConnectionServerName = "connectionServerName";
        public const string ConnectionDatabaseName = "connectionDatabaseName";
        public const string ConnectionUserName = "connectionUserName";
        public const string ConnectionPassword = "connectionPassword";
    }

    /// <summary>
    /// The possible result from an operation.
    /// </summary>
    [DataContract(Namespace = "http://schemas.microsoft.com/windowsazure")]
    public enum OperationResult
    {
        [EnumMember]
        InProgress,

        [EnumMember]
        Succeeded,

        [EnumMember]
        Failed
    }

    // Note that these classes should not require a specific order of data members.
    // Any order should be accepted when deserializing the response from the resource provider.

    /// <summary>
    /// Settings of the cloud service that are sent in the resource-level operations.
    /// </summary>
    [DataContract(Namespace = "http://schemas.microsoft.com/windowsazure")]
    public class CloudServiceSettings : IExtensibleDataObject
    {
        /// <summary>
        /// The geo location of the cloud service.
        /// </summary>
        [DataMember]
        public string GeoLocation { get; set; }

        public ExtensionDataObject ExtensionData { get; set; }
    }

    /// <summary>
    /// Error information about a failed operation.
    /// </summary>
    [DataContract(Name = "Error", Namespace = "http://schemas.microsoft.com/windowsazure")]
    public class ErrorData : IExtensibleDataObject
    {
        /// <summary>
        /// The HTTP error code.
        /// </summary>
        [DataMember(IsRequired = true)]
        public int HttpCode { get; set; }

        /// <summary>
        /// The error message.
        /// </summary>
        [DataMember(IsRequired = true)]
        public string Message { get; set; }

        public ExtensionDataObject ExtensionData { get; set; }
    }

    /// <summary>
    /// Status about an operation.
    /// </summary>
    [DataContract(Namespace = "http://schemas.microsoft.com/windowsazure")]
    public class OperationStatus : IExtensibleDataObject
    {
        /// <summary>
        /// The error code. This is not necessarily an integer.
        /// </summary>
        [DataMember(IsRequired = true)]
        public OperationResult Result { get; set; }

        /// <summary>
        /// The error information for an unhealthy resource.
        /// CS manager only passes this field to callers.
        /// </summary>
        [DataMember]
        public ErrorData Error { get; set; }

        public ExtensionDataObject ExtensionData { get; set; }
    }

    /// <summary>
    /// Resource information, as sent to the resource provider for the resource-level operations.
    /// </summary>
    [DataContract(Name = "Resource", Namespace = "http://schemas.microsoft.com/windowsazure")]
    public class ResourceInput : IExtensibleDataObject
    {
        /// <summary>
        /// The cloud service settings sent along with this resource input.
        /// </summary>
        [DataMember]
        public CloudServiceSettings CloudServiceSettings { get; set; }

        /// <summary>
        /// The type of the resource.
        /// </summary>
        [DataMember]
        public string Type { get; set; }

        /// <summary>
        /// The plan of the resource.
        /// </summary>
        [DataMember]
        public string Plan { get; set; }

        /// <summary>
        /// The incarnation ID of the resource.
        /// </summary>
        [DataMember]
        public int IncarnationId { get; set; }

        /// <summary>
        /// The schema version of the intrinsic settings.
        /// </summary>
        [DataMember]
        public string SchemaVersion { get; set; }

        /// <summary>
        /// The intrinsic settings of the resource.
        /// The values and schema of this field are defined by the resource provider.
        /// </summary>
        [DataMember]
        public XmlNode[] IntrinsicSettings { get; set; }

        public ExtensionDataObject ExtensionData { get; set; }
    }

    /// <summary>
    /// Resource information, as returned by the resource provider.
    /// </summary>
    [DataContract(Name = "Resource", Namespace = "http://schemas.microsoft.com/windowsazure")]
    public class ResourceOutput : IExtensibleDataObject
    {
        /// <summary>
        /// The cloud service settings.
        /// This field is only filled in by the resource-level APIs (PUT/DELETE resource), not by the cloud-service-level APIs.
        /// </summary>
        [DataMember]
        public CloudServiceSettings CloudServiceSettings { get; set; }

        /// <summary>
        /// The name of the resource. It is unique within a cloud service.
        /// This field is only filled in by the cloud-service-level APIs (PUT/GET/DELETE cloud service).
        /// In the resource-level APIs, the resource name is already present in the URI of the request.
        /// </summary>
        [DataMember]
        public string Name { get; set; }

        /// <summary>
        /// The type of the resource.
        /// </summary>
        [DataMember]
        public string Type { get; set; }

        /// <summary>
        /// The plan of the resource.
        /// </summary>
        [DataMember]
        public string Plan { get; set; }

        /// <summary>
        /// The incarnation ID of the resource.
        /// </summary>
        [DataMember]
        public int IncarnationId { get; set; }

        /// <summary>
        /// The schema version of the intrinsic settings.
        /// </summary>
        [DataMember]
        public string SchemaVersion { get; set; }

        /// <summary>
        /// The intrinsic settings of the resource.
        /// The values and schema of this field are defined by the resource provider.
        /// </summary>
        [DataMember]
        public XmlNode[] IntrinsicSettings { get; set; }

        /// <summary>
        /// The output of of a resource, can be null.
        /// The values and schema of this field are defined by the resource provider.
        /// </summary>
        [DataMember]
        public OutputItemList OutputItems { get; set; }

        /// <summary>
        /// The state of the resource.
        /// </summary>
        [DataMember]
        public ResourceState State { get; set; }

        /// <summary>
        /// The sub-state of the resource. The possible values to this field are defined by the resource provider.
        /// </summary>
        [DataMember]
        public string SubState { get; set; }

        /// <summary>
        /// Status about an operation on this resource.
        /// </summary>
        [DataMember(IsRequired = true)]
        public OperationStatus OperationStatus { get; set; }

        public ExtensionDataObject ExtensionData { get; set; }
    }

    /// <summary>
    /// List of resources, as returned by the resource provider.
    /// </summary>
    [CollectionDataContract(Name = "Resources", Namespace = "http://schemas.microsoft.com/windowsazure")]
    public class ResourceOutputCollection : List<ResourceOutput>
    {
        public ResourceOutputCollection()
        {
        }

        public ResourceOutputCollection(IEnumerable<ResourceOutput> resources)
            : base(resources)
        {
        }

        public ResourceOutput Find(string resourceType, string resourceName)
        {
            return this.Find(res =>
                string.Equals(res.Type, resourceType, StringComparison.InvariantCultureIgnoreCase) &&
                string.Equals(res.Name, resourceName, StringComparison.InvariantCultureIgnoreCase));
        }
    }

    /// <summary>
    /// Cloud service information, as returned by the resource provider.
    /// </summary>
    [DataContract(Name = "CloudService", Namespace = "http://schemas.microsoft.com/windowsazure")]
    public class CloudServiceOutput : IExtensibleDataObject
    {
        /// <summary>
        /// The incarnation ID of this request.
        /// </summary>
        [DataMember(IsRequired = true)]
        public int IncarnationId { get; set; }

        /// <summary>
        /// The geo location of the cloud service.
        /// </summary>
        [DataMember(IsRequired = true)]
        public string GeoLocation { get; set; }

        /// <summary>
        /// The resources of the cloud service.
        /// </summary>
        [DataMember(IsRequired = true)]
        public ResourceOutputCollection Resources { get; set; }

        public ExtensionDataObject ExtensionData { get; set; }
    }


    [CollectionDataContract(Name = "CloudServices", Namespace = "http://schemas.microsoft.com/windowsazure")]
    public class CloudServiceOutputCollection : List<CloudServiceOutput>
    {
        public CloudServiceOutputCollection()
        {
        }

        public CloudServiceOutputCollection(IEnumerable<CloudServiceOutput> cloudServices)
            : base(cloudServices)
        {
        }
    }

    [DataContract(Namespace = "http://schemas.microsoft.com/windowsazure")]
    public class OutputItem : IExtensibleDataObject
    {
        public ExtensionDataObject ExtensionData { get; set; }

        [DataMember(EmitDefaultValue = false)]
        public string Key { get; set; }

        [DataMember(EmitDefaultValue = false)]
        public string Value { get; set; }
    }


    [CollectionDataContract(Name = "Output", ItemName = "OutputItem", Namespace = "http://schemas.microsoft.com/windowsazure")]
    public class OutputItemList : List<OutputItem>
    {
        public OutputItemList()
        {
        }

        public OutputItemList(IEnumerable<OutputItem> outputs)
            : base(outputs)
        {
        }
    }

    /// <summary>
    /// The states that are reported by the resource provider.
    /// Resource providers should only return values in this enumeration, although that is not enforced.
    /// </summary>
    public enum ResourceState
    {
        /// <summary>
        /// The resource state is unkown because an error occurred when calling the resource provider.
        /// </summary>
        Unknown,

        /// <summary>
        /// The resource provider has no record of this resource.
        /// </summary>
        NotFound,

        /// <summary>
        /// The resource is started.
        /// </summary>
        Started,

        /// <summary>
        /// The resource is stopped.
        /// </summary>
        Stopped,

        /// <summary>
        /// The resource is paused.
        /// </summary>
        Paused,
    }

    [DataContract(Namespace = "http://schemas.microsoft.com/windowsazure")]
    public class EntityEvent : IExtensibleDataObject
    {
        [DataMember(EmitDefaultValue = false)]
        public Guid EventId { get; set; }

        [DataMember(EmitDefaultValue = false)]
        public string EntityType { get; set; } // TODO: noty string

        [DataMember(EmitDefaultValue = false)]
        public string EntityState { get; set; } // TODO: not really a string

        [DataMember(EmitDefaultValue = false)]
        public Guid OperationId { get; set; }

        [DataMember(EmitDefaultValue = false)]
        public bool IsAsync { get; set; }

        public ExtensionDataObject ExtensionData { get; set; }
    }

    /// <summary>
    /// Resource provider operations.
    /// </summary>
    [ServiceContract]
    public interface IResourceProvider
    {
        [OperationContract(AsyncPattern = true)]
        [WebInvoke(Method = "PUT", UriTemplate = "/subscriptions/{subscriptionId}/cloudservices/{cloudServiceName}/resources/{resourceType}/{resourceName}")]
        IAsyncResult BeginPutResource(string subscriptionId, string cloudServiceName, string resourceType, string resourceName, ResourceInput resourceInput, AsyncCallback callback, object state);
        ResourceOutput EndPutResource(IAsyncResult result);

        [OperationContract(AsyncPattern = true)]
        [WebGet(UriTemplate = "/subscriptions/{subscriptionId}/cloudservices/{cloudServiceName}")]
        IAsyncResult BeginGetCloudServiceResources(string subscriptionId, string cloudServiceName, AsyncCallback callback, object state);
        CloudServiceOutput EndGetCloudServiceResources(IAsyncResult result);

        [OperationContract(AsyncPattern = true)]
        [WebInvoke(Method = "DELETE", UriTemplate = "/subscriptions/{subscriptionId}/cloudservices/{cloudServiceName}/resources/{resourceType}/{resourceName}")]
        IAsyncResult BeginDeleteResource(string subscriptionId, string cloudServiceName, string resourceType, string resourceName, AsyncCallback callback, object state);
        ResourceOutput EndDeleteResource(IAsyncResult result);
    }
}
