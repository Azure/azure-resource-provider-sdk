class Subscription < ActiveRecord::Base
	has_many :cloud_services
end
