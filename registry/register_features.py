from sqlalchemy import create_engine, text

# UPDATE PASSWORD if needed
engine = create_engine(
    "postgresql://postgres:Dmml123@localhost:5432/RecoMart_DB"
)

query = """
INSERT INTO feature_registry
(feature_name, source_table, transformation_logic, feature_version)
VALUES
('user_activity_count',
 'ecommerce_events',
 'COUNT(*) GROUP BY user_id',
 'v1'),

('avg_price_per_user',
 'ecommerce_events',
 'AVG(price) GROUP BY user_id',
 'v1'),

('item_popularity',
 'ecommerce_events',
 'COUNT(*) GROUP BY product_id',
 'v1'),

('user_item_interaction_count',
 'ecommerce_events',
 'COUNT(*) GROUP BY user_id, product_id',
 'v1')
ON CONFLICT (feature_name) DO NOTHING;
"""

with engine.begin() as conn:
    conn.execute(text(query))

print("Feature registry updated successfully")
