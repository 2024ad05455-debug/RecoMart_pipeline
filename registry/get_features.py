from sqlalchemy import create_engine, text

# UPDATE PASSWORD if needed
engine = create_engine(
    "postgresql://postgres:Dmml123@localhost:5432/RecoMart_DB"
)

user_id = 100  # example user
product_id = 1  # example product

query = """
SELECT
    uf.user_id,
    uf.activity_count,
    uf.avg_price AS user_avg_price,
    it.interaction_count AS item_popularity
FROM user_features uf
JOIN item_features it
ON it.product_id = :product_id
WHERE uf.user_id = :user_id;
"""

with engine.connect() as conn:
    result = conn.execute(
        text(query),
        {"user_id": user_id, "product_id": product_id}
    )

    for row in result:
        print(dict(row))
