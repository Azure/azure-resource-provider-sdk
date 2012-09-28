class ApplicationController < ActionController::Base
  protect_from_forgery

    before_filter :header_javascript
     
    def header_javascript
    response.headers['Content-type'] = 'text/xml'
    end


end
