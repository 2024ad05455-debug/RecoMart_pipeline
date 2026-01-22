import json
import pandas as pd
import logging
from sqlalchemy import create_engine
from datetime import datetime
import os

DB_USER = "postgres"
DB_PASSWORD = "Dmml123"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "RecoMart_DB"

TABLE_NAME = "products"
BASE_RAW_PATH = "data/raw/api/product_data"
LOG_FILE = "logs/products_postgres_load.log"

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_products():
    try:
        ingest_date = datetime.now().strftime("%Y-%m-%d")
        json_path = f"{BASE_RAW_PATH}/ingest_date={ingest_date}/products.json"

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        df = pd.DataFrame(data["products"])[
            ["id", "title", "brand", "category", "price", "rating", "stock"]
        ]
        df.rename(columns={"id": "product_id"}, inplace=True)

        engine = create_engine(
            f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

        logging.info(f"Rows to insert: {len(df)}")

        with engine.begin() as conn:
            df.to_sql(TABLE_NAME, conn, if_exists="append", index=False)

        logging.info("Product data loaded into PostgreSQL successfully")

    except Exception as e:
        logging.error(f"Product PostgreSQL load failed: {str(e)}")
        raise

if __name__ == "__main__":
    load_products()
