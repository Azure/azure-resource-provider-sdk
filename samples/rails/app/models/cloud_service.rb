class CloudService < ActiveRecord::Base
	 has_many :resources, :dependent => :destroy 
	 belongs_to :subscriptions
end
