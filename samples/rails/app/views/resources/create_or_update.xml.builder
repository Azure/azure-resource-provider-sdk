xml.instruct!
xml.Resource "xmlns"=> "http://schemas.microsoft.com/windowsazure" do
  xml.CloudServiceSettings #do
    #@basic_params[:CloudServiceSettings].each do |key,value|
     # xml.tag!(key.to_s,value)
     #xml.GeoLocation ""
    #end
  #end
  #plan is not expected back in the current sandbox build.
  #xml.Plan @basic_params[:Plan]
  xml.Etag @basic_params[:Etag]
  xml.IntrinsicSettings do
    xml.Key "key"
    xml.Value "Value"
  end
  xml.Name @resource.name
  
  xml.OperationStatus do
    @basic_params[:OperationStatus].each do |key,value|
      xml.tag!(key.to_s,value)
    end
  end
  xml.OutputItems do
    @basic_params[:OutputItems].each do |item|
      xml.OutputItem do
        xml.Key item[:key]
        xml.Value item[:value]
      end
    end
  end
  xml.Plan @basic_params[:Plan]
  xml.State "Started"
  xml.SubState "Waiting for your order"
end
logger.info xml.target!
