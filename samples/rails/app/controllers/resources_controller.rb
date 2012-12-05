#
# Copyright 2011 Microsoft Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


require 'rubygems'
require 'base64'
require 'cgi'
#require 'hmac-sha1'

class ResourcesController < ApplicationController
	#/Subscriptions/:subscription_id/cloudservices/#cloud_service_id/resources/:id - PUT
	def create_or_update
		#called to update and create resources. response.headers["Content-Type"] = 'text/xml'
		logger.info "incoming request is : #{request.raw_post}"
		@basic_params = params[:Resource]
		#first lets find cloud service from the id. 
		@subscription = Subscription.find_or_create_by_subscription_id(params[:subscription_id])
		@cloud_service = CloudService.where("name = ? AND subscription_id = ?",params[:cloud_service_id],@subscription.id).first_or_initialize
		@cloud_service.name = params[:cloud_service_id]
		@cloud_service.subscription_id = @subscription.id
		if @basic_params[:CloudServiceSettings]
			@cloud_service.geo_region = @basic_params[:CloudServiceSettings][:GeoRegion]
		end
		@cloud_service.save!
	
		#@resource = Resource.find_or_create_by_name_and_cloudservice_id(:name => params[:id], :cloudservice_id => @cloud_service.id)
		@resource = Resource.where("name = ? AND cloud_service_id = ?",params[:id],@cloud_service.id).first_or_initialize
		#@resource.save_params @basic_params
		logger.info ("incarnation ids are different - trying to update the resource")
		@resource.name = params[:id]
		@resource.cloud_service_id = @cloud_service.id
		@resource.resource_type = params[:resourcetype]
		@resource.connection_url = "http://testrails/randomizer/#{params[:id]}"
		@resource.password = "123456"
		@resource.salt = "XYZ_3#{params[:subscription_id]}_#{params[:cloud_service_id]}_#{params[:id]}"
		@resource.incarnation_id = @basic_params[:IncarnationID]
		@resource.schema_version = @basic_params[:SchemaVersion]
		@resource.plan = @basic_params[:Plan]
		@resource.version = @basic_params[:Version]
		@resource.intrinsic_settings = @basic_params[:IntrinsicSettings]
		@resource.promotion_code = @basic_params[:PromotionCode]
		logger.info "saving the resource #{@resource}"
		@resource.save!	

		logger.info "generating output items"
		@output_items = Array.new
		@output_item = Hash.new
		@output_item["key"] = "connection_url"
		@output_item["value"] = @resource.connection_url
		@output_items << @output_item
		@output_item = Hash.new
		@output_item["key"] = "key"
		@output_item["value"] = @resource.password
		@output_items << @output_item
		@basic_params[:OutputItems] = @output_items
		@operation_status = Hash.new
		@operation_status["Result"] = "Succeeded"
		@basic_params["OperationStatus"] = @operation_status
		@basic_params["SubState"] = " Here one can define all kinds of usage values" 
		@output = Hash.new
		@output[:Resource] = @basic_params

		respond_to do |format|
			format.html {render :template => "resources/create_or_update.xml.builder", :layout => false}
			format.xml
   		end
	end

	# match 'subscriptions/:subscription_id/cloudservices/:cloud_service_id/resources/:resource_type/:id/SsoToken'=> via [:post]
	def sso
		# will be invokded when the user clicks the manage button in the portal.  This will create the token and pass it to Azure along
		# with the timestamp.
		@secret_key = "Change this key to some other value if you are using this sample"
		@signature = "#{params[:subscription_id]}:#{params[:cloud_service_id]}:#{params[:id]}"
		@token = Digest::SHA1.hexdigest(@signature) #HMAC::SHA1.new(@secret_key)
		#token.update(@signature)
		@timestamp = DateTime.now
		respond_to do |format|
			format.html {render :template => "resources/sso.xml.builder", :layout => false}
			format.xml
   		end
	end

	# match 'Sso' => 'resources#sso_view', via => [:get]
	def sso_view
		# used to show the single signed on view for a given resource. 
		@show_data = false
		# get the parameters and encrypt it using the same key. 
		@signature = "#{params[:subid]}:#{params[:cloudservicename]}:#{params[:resourcename]}"
		@secret_key = "Change this key to some other value if you are using this sample"
		@token_now = Digest::SHA1.hexdigest(@signature) #HMAC::SHA1.new(@secret_key)
		#token_now.update(@signature)
		if (@token_now == params[:token])
			@timestamp_now = DateTime.now
			logger.info("the tokens match, check for timestamp match the time now is #{@timestamp_now}")
			if ((@timestamp_now - params[:timestamp].to_datetime)/1.minute < 10)
				logger.info "The time difference is less than 10 minutes, send back http request"
				@show_data = true
			end
		else
			logger.info "Oops token do not match"
		end
	end
	#'subscriptions/:subscription_id/cloudservices/:cloud_service_id/resources/:resource_type/:id' 
	def show
		@subscription = Subscription.find(:first,"subscription_id =?", params[:subscription_id])

		unless @subscription
			# we have not get a register event on this, return with an error
			render :nothing => true, :status => :not_found 
			return
		end	
		@cloud_service = CloudService.find_by_subscription_id_and_name(@subscription.id,params[:cloud_service_id])
		unless @cloud_service
			render :nothing => true, :status => :not_found 
		end
		@resource = Resource.find_by_cloud_service_id_and_name_and_resource_type(@cloud_service.id,params[:id],params[:resource_type])
		unless @resource
			render :nothing => true, :status => :not_found 
		end
		respond_to do |format|
			format.html { render :xml => @resource, :root => "Resource",  :skip_types => true,:camelize => true, :except => [:id,:subscription_id]}
			format.xml  { render :xml => @resource, :root => "Resource",  :skip_types => true,:camelize => true, :except => [:id,:subscription_id]}
      	end
    end
    def destroy
    	@subscription = Subscription.find(:first,"subscription_id =?", params[:subscription_id])
		unless @subscription
			# we have not get a register event on this, return with an error
			render :nothing => true, :status => :not_found 
			return
		end	
    	@cloud_service = CloudService.find_by_subscription_id_and_name(@subscription.id,params[:cloud_service_id])
		unless @cloud_service
			render :nothing => true, :status => :not_found 
			return
		end
		@resource = Resource.find_by_cloud_service_id_and_name_and_resource_type(@cloud_service.id,params[:id],params[:resource_type])
		unless @resource
			render :nothing => true, :status => :not_found 
			return
		end
		@resource.destroy
	end
end