class CreateProducts < ActiveRecord::Migration
  def change
    create_table :products do |t|
      t.string :name
      t.string :token
      t.string :subscription
      t.string :service

      t.timestamps
    end
  end
end
