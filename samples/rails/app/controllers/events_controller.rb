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

class EventsController < ApplicationController
	def create
		# This is called when any subscription messages are sent 
		logger.info "incoming request is : #{request.raw_post}"
		@basic_params = params[:EntityEvent]
		@event = Event.find_by_operation_id(@basic_params[:OperationId])
		logger.info("Create call for events: with params: #{@basic_params}")
		unless @event
			logger.info("Creating a new event with id: params[:id]")
			@event = Event.new
			@event.subscription_id = params[:id]
			@event.entity_state = @basic_params[:EntityState]
			@event.operation_id  = @basic_params[:OperationId]
			if (@basic_params[:EntityId])
			  @event.subscription_creation_date = @basic_params[:EntityId][:Created]
		    end
		    logger.info("saving a new event with op_id: params[:operation_id]")
			@event.save!
			if (@event.entity_state == "Registered")
				 logger.info("Registered event, create a subscription")
				@subscription = Subscription.new
				@subscription.state = 1 #SUBSCRIPTION_STATE_REGISTERED
				@subscription.subscription_id = params[:id]
				if (@basic_params[:EntityId])
			  		@subscription.created_date = @basic_params[:EntityId][:Created]
			  	end
			  	@subscription.save!
			else
				logger.info("State change: update subscription")
				@subscription = Subscription.find_by_subscription_id(params[:id])
				if (@event.entity_state == "Disabled")
					@Subscription.state = 2 #
				elsif (@event.entity_state == "Deleted")
					@Subscription.state = 3 #SUBSCRIPTION_STATE_DELETED
				end
				@subscription.save! if @subscription
			end
			
      	end
      	respond_to do |format|
				format.html { render :xml => @event}
				format.xml  { render :xml => @event} 
      		end
	end
	def list
		@events = Event.all
		respond_to do |format|
          format.html { render :xml => @events}
          format.xml  { render :xml => @events}
     	end
	end
end