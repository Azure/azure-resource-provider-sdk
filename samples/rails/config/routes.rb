Randomize::Application.routes.draw do
  # The priority is based upon order of creation:
  # first created -> highest priority.
  resources :subscriptions do
    #resources :cloudservices #do
     #resources :resources
    #end
  end 
  match '/:id/Events' => 'events#create', :via=>[:get, :post]
  match 'subscriptions/:id/Events' => 'events#create', :via=>[:get, :post]
  match '/:id/Events/list' => 'events#list'
  match 'subscriptions/:subscription_id/cloudservices' => 'CloudServices#index' , :via => [:get]
  match 'subscriptions/:subscription_id/cloudservices/:id' => 'CloudServices#show', :via => [:get]
  match 'subscriptions/:subscription_id/cloudservices/:cloud_service_id/resources/:resource_type/:id' => 'resources#show' , :via => [:get]
  match 'subscriptions/:subscription_id/cloudservices/:cloud_service_id/resources/:resource_type/:id' => 'resources#create_or_update' , :via => [:put]
  match 'subscriptions/:subscription_id/cloudservices/:cloud_service_id/resources/:resource_type/:id/SsoToken' => 'resources#sso' , :via => [:post]
  match 'subscriptions/:subscription_id/cloudservices/:cloud_service_id/resources/:resource_type/:id' => 'resources#destroy' , :via => [:delete]
  match 'Sso' => 'resources#sso_view', :via => [:get]
  # Sample of regular route:
  #   match 'products/:id' => 'catalog#view'
  # Keep in mind you can assign values other than :controller and :action

  # Sample of named route:
  #   match 'products/:id/purchase' => 'catalog#purchase', :as => :purchase
  # This route can be invoked with purchase_url(:id => product.id)

  # Sample resource route (maps HTTP verbs to controller actions automatically):
  #   resources :products

  # Sample resource route with options:
  #   resources :products do
  #     member do
  #       get 'short'
  #       post 'toggle'
  #     end
  #
  #     collection do
  #       get 'sold'
  #     end
  #   end

  # Sample resource route with sub-resources:
  #   resources :products do
  #     resources :comments, :sales
  #     resource :seller
  #   end

  # Sample resource route with more complex sub-resources
  #   resources :products do
  #     resources :comments
  #     resources :sales do
  #       get 'recent', :on => :collection
  #     end
  #   end

  # Sample resource route within a namespace:
  #   namespace :admin do
  #     # Directs /admin/products/* to Admin::ProductsController
  #     # (app/controllers/admin/products_controller.rb)
  #     resources :products
  #   end

  # You can have the root of your site routed with "root"
  # just remember to delete public/index.html.
  # root :to => 'welcome#index'

  # See how all your routes lay out with "rake routes"

  # This is a legacy wild controller route that's not recommended for RESTful applications.
  # Note: This route will make all actions in every controller accessible via GET requests.
  # match ':controller(/:action(/:id))(.:format)'
end
