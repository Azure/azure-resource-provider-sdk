using System;
using System.Runtime.Serialization;

namespace ResourceProvidR.Models
{
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
}