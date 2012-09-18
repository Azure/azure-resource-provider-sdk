class ProviderController < ApplicationController
	
	#PUT - https:// <registered-resource-provider-endpoint>/ subscriptions/{subscriptionId}/cloudservices/{cloud-service-name}/Resources/{resource-type}/{resource-name}
	def create
		logger.info (" call received with params: #{params}")
		respond_to do |format|
            # format.html 
      		format.html { render json:params} 
      	end
	end

end
