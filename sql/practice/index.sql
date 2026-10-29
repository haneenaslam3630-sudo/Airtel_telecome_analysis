CREATE INDEX IF NOT EXISTS ix_orders_customers
ON shop_orders(customer_id);