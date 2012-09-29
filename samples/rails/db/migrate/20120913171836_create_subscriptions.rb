class CreateSubscriptions < ActiveRecord::Migration
  def change
    create_table :subscriptions do |t|
      t.string :subscription_id
      t.string :created_date
      t.integer :state
      t.timestamps
    end
  end
end
