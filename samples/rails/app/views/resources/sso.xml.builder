xml.instruct!
xml.SsoToken "xmlns"=> "http://schemas.microsoft.com/windowsazure" do
	xml.Token token 
	xml.TimeStamp timestamp
end