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

class CloudServicesController < ApplicationController
	def index
		@subscription = Subscription.find(:first,"subscription_id =?", params[:subscription_id])
		unless @subscription
			# we have not get a register event on this, return with an error
			render :nothing => true, :status => :not_found 
			return
		end	
		@cloud_services = CloudService.where('subscription_id = ?',@subscription.id)
		unless @cloud_services
			render :nothing => true, :status => :not_found 
			return
		end
	     respond_to do |format|
				format.html { render :xml => @cloud_services, :root => "CloudServices",  :skip_types => true,:camelize => true, :include => {:resources => {:camelize => true, :skip_types => true,:skip_instructions => true, :except => [:cloud_service_id,:intrinsic_settings]}}, :except => [:id,:subscription_id]}
				format.xml  { render :xml => @cloud_services, :root => "CloudServices",  :skip_types => true,:camelize => true, :include => {:resources => {:camelize => true, :skip_types => true,:skip_instructions => true, :except => [:cloud_service_id,:intrinsic_settings]}}, :except => [:id,:subscription_id]}
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
		@cloud_service.destroy
	end
	# Route -> subscriptions/:subscription_id/cloudservices/:id
	def show
		@subscription = Subscription.find_by_subscription_id( params[:subscription_id])
		unless @subscription
			# we have not get a register event on this, return with an error
			render :nothing => true, :status => :not_found 
			return
		end	
		@cloud_service = CloudService.find_by_subscription_id_and_name(@subscription.id,params[:id])
		unless @cloud_service
			render :nothing => true, :status => :not_found 
			return
		end
		respond_to do |format|
			format.html {render :template => "cloud_services/show.xml.builder", :layout => false} #{ render :xml => @cloud_service, :root => "CloudService",  :skip_types => true,:camelize => true, :include => {:resources => {:camelize => true, :skip_types => true,:skip_instructions => true, :except => [:cloud_service_id,:intrinsic_settings]}}, :except => [:id,:subscription_id]}
			format.xml  #{ render :xml => @cloud_service, :root => "CloudService",  :skip_types => true,:camelize => true, :include => {:resources => {:camelize => true, :skip_types => true,:skip_instructions => true, :except => [:cloud_service_id,:intrinsic_settings]}}, :except => [:id,:subscription_id]}
		end
	end      	
end