using System;
using System.Collections.Generic;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.ServiceModel.Web;
using System.Xml;

namespace Microsoft.WindowsAzure.CloudServiceManagement.ResourceProviderCommunication
{
    /// <summary>
    /// Type representing identifier of Entity under subscription.
    /// </summary>
    [DataContract(Namespace = "http://schemas.datacontract.org/2004/07/Microsoft.Cis.DevExp.Services.Rdfe.ServiceManagement")]
    public class EntityId
    {
        [DataMember(EmitDefaultValue = false, IsRequired = true, Order = 0)]
        public string Id { get; set; }

        [DataMember(EmitDefaultValue = false, IsRequired = false, Order = 1)]
        public DateTime Created { get; set; }
    }

    /// <summary>
    /// State of entity.
    /// </summary>
    [DataContract(Namespace = "http://schemas.datacontract.org/2004/07/Microsoft.Cis.DevExp.Services.Rdfe.ServiceManagement")]
    public enum EntityState
    {
        [EnumMember]
        Deleted,

        [EnumMember]
        Enabled,

        [EnumMember]
        Disabled,

        [EnumMember]
        Migrated,

        [EnumMember]
        Updated,

        [EnumMember]
        Registered,

        [EnumMember]
        Unregistered
    }

    [DataContract(Namespace = "http://schemas.datacontract.org/2004/07/Microsoft.Cis.DevExp.Services.Rdfe.ServiceManagement")]
    public class EntityEvent
    {
        [DataMember(EmitDefaultValue = false, IsRequired = true, Order = 0)]
        public string EventId { get; set; }

        [DataMember(EmitDefaultValue = false, Order = 1)]
        public string ListenerId { get; set; }

        [DataMember(EmitDefaultValue = false, Order = 2)]
        public string EntityType { get; set; }

        [DataMember(EmitDefaultValue = false, Order = 3)]
        public EntityState EntityState { get; set; }

        [DataMember(EmitDefaultValue = false, Order = 4)]
        public EntityId EntityId { get; set; }

        [DataMember(EmitDefaultValue = false, Order = 5)]
        public string OperationId { get; set; }

        [DataMember(EmitDefaultValue = false, Order = 6)]
        public bool IsAsync { get; set; }

        public EntityEvent CreateCopy(string listenerId)
        {
            EntityEvent copy = base.MemberwiseClone() as EntityEvent;
            copy.ListenerId = listenerId;
            return copy;
        }
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

    /// <summary>
    /// Settings of the cloud service that are sent in the resource-level operations.
    /// </summary>
    [DataContract(Namespace = "http://schemas.microsoft.com/windowsazure")]
    public class CloudServiceSettings : IExtensibleDataObject
    {
        /// <summary>
        /// The geo region of the cloud service.
        /// </summary>
        [DataMember]
        public string GeoRegion { get; set; }

        /// <summary>
        /// The user's email.
        /// </summary>
        [DataMember]
        public string Email { get; set; }

        public ExtensionDataObject ExtensionData { get; set; }
    }

    /// <summary>
    /// Usage of a certain meter.
    /// For example, capacity (used/total), emails sent (sent/monthly limit), etc.
    /// </summary>
    [DataContract(Namespace = "http://schemas.microsoft.com/windowsazure")]
    public class UsageMeter : IExtensibleDataObject
    {
        /// <summary>
        /// The meter name.
        /// </summary>
        [DataMember(IsRequired = true)]
        public string Name { get; set; }

        /// <summary>
        /// The unit of this meter.
        /// </summary>
        [DataMember(IsRequired = true)]
        public string Unit { get; set; }

        /// <summary>
        /// The included quantity.
        /// </summary>
        [DataMember(IsRequired = true)]
        public string Included { get; set; }

        /// <summary>
        /// The used quantity.
        /// </summary>
        [DataMember(IsRequired = true)]
        public string Used { get; set; }

        public ExtensionDataObject ExtensionData { get; set; }
    }

    /// <summary>
    /// List of usage meters, as returned by the resource provider.
    /// </summary>
    [CollectionDataContract(Name = "UsageMeters", Namespace = "http://schemas.microsoft.com/windowsazure")]
    public class UsageMeterCollection : List<UsageMeter>
    {
        public UsageMeterCollection()
        {
        }

        public UsageMeterCollection(IEnumerable<UsageMeter> meters)
            : base(meters)
        {
        }
    }

    [DataContract(Namespace = "http://schemas.microsoft.com/windowsazure")]
    public class OutputItem : IExtensibleDataObject
    {
        /// <summary>
        /// The key of the output item.
        /// </summary>
        [DataMember(IsRequired = true)]
        public string Key { get; set; }

        /// <summary>
        /// The value of the output item.
        /// </summary>
        [DataMember(IsRequired = true)]
        public string Value { get; set; }

        public ExtensionDataObject ExtensionData { get; set; }
    }

    /// <summary>
    /// Class representing a list of key-value-pairs with the resource output.
    /// </summary>
    [CollectionDataContract(Name = "OutputItems", ItemName = "OutputItem", Namespace = "http://schemas.microsoft.com/windowsazure")]
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
        /// The etag of the resource.
        /// </summary>
        [DataMember]
        public int ETag { get; set; }

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
        /// The resource promotion code.
        /// </summary>
        [DataMember]
        public string PromotionCode { get; set; }

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
        /// 
        /// This is here, despite of not being used in the code, since, we want RPs to return the output as the same as input, and 
        /// we will have option to use it in the future.
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
        /// The etag of the resource.
        /// </summary>
        [DataMember]
        public int ETag { get; set; }

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
        /// The resource promotion code. The resource provider is not required to return this field.
        /// The field is not returned to Portal nor used by RDFE. It is only defined here in case we decide to use it in the future.
        /// </summary>
        [DataMember]
        public string PromotionCode { get; set; }

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
        public string State { get; set; }

        /// <summary>
        /// The sub-state of the resource. The possible values to this field are defined by the resource provider.
        /// </summary>
        [DataMember]
        public string SubState { get; set; }

        /// <summary>
        /// The usage meters of the resource. The specific meters are defined by the resource provider.
        /// This field is optional.
        /// </summary>
        [DataMember]
        public UsageMeterCollection UsageMeters { get; set; }

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
        /// The geo region of the cloud service.
        /// 
        /// This is here, despite of not being used in the code, since, we want RPs to return the output as the same as input, and 
        /// we will have option to use it in the future.
        /// </summary>
        [DataMember(IsRequired = true)]
        public string GeoRegion { get; set; }

        /// <summary>
        /// The resources of the cloud service.
        /// </summary>
        [DataMember(IsRequired = true)]
        public ResourceOutputCollection Resources { get; set; }

        public ExtensionDataObject ExtensionData { get; set; }
    }

    /// <summary>
    /// Class with the details to generate a token for single-sign-on.
    /// </summary>
    [DataContract(Namespace = "http://schemas.microsoft.com/windowsazure")]
    public class SsoToken : IExtensibleDataObject
    {
        /// <summary>
        /// The token.
        /// </summary>
        [DataMember(IsRequired = true)]
        public string Token { get; set; }

        /// <summary>
        /// Timestamp to indicate when the token was generated.
        /// </summary>
        [DataMember(IsRequired = true)]
        public string TimeStamp { get; set; }

        public ExtensionDataObject ExtensionData { get; set; }
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
}