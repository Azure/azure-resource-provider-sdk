class CreateCloudServices < ActiveRecord::Migration
  def change
    create_table :cloud_services do |t|
      t.string :name
      t.references :subscription
      t.string :geo_region
	  t.timestamps
    end
  end
end