xml.instruct!
xml.SsoToken "xmlns"=> "http://schemas.microsoft.com/windowsazure" do
	xml.TimeStamp @timestamp
	xml.Token @token 
end
logger.info xml.target!