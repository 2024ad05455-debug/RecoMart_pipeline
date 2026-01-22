from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql://postgres:Dmml123@localhost:5432/RecoMart_DB"
)

queries = [
    """
    INSERT INTO user_features
    SELECT user_id, COUNT(*), AVG(price)
    FROM ecommerce_events
    GROUP BY user_id
    ON CONFLICT (user_id)
    DO UPDATE SET
        activity_count = EXCLUDED.activity_count,
        avg_price = EXCLUDED.avg_price;
    """,
    """
    INSERT INTO item_features
    SELECT product_id, COUNT(*), AVG(price)
    FROM ecommerce_events
    GROUP BY product_id
    ON CONFLICT (product_id)
    DO UPDATE SET
        interaction_count = EXCLUDED.interaction_count,
        avg_price = EXCLUDED.avg_price;
    """
]

with engine.begin() as conn:
    for q in queries:
        conn.execute(text(q))

print("Feature engineering completed successfully")
