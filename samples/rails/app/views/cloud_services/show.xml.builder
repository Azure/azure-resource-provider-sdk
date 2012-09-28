xml.instruct!
xml.CloudService "xmlns"=> "http://schemas.microsoft.com/windowsazure" do
  xml.GeoLocation "usnorth"
  xml.Resources do
    @cloud_service.resources.each do |resource|
      xml.Resource do
        xml.Etag 1
        xml.Name resource.name
        xml.OperationStatus do
          xml.Result "Succeeded"
        end
        xml.Plan resource.plan
        xml.State "Started"
        xml.SubState "Waiting for your order"
        xml.Type "testrprails"
      end
    end
  end
end
logger.info xml.target!