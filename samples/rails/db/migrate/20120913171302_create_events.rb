class CreateEvents < ActiveRecord::Migration
  def change
    create_table :events do |t|
      t.string :subscription_id
      t.string :entity_state
      t.string :subscription_creation_date
      t.string :operation_id
      t.timestamps
    end
  end
end
