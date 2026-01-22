import pandas as pd
import logging
from sqlalchemy import create_engine
from datetime import datetime
import os

# ---------------- CONFIG ----------------
DB_USER = "postgres"
DB_PASSWORD = "Dmml123"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "RecoMart_DB"

TABLE_NAME = "ecommerce_events"
BASE_RAW_PATH = "data/raw/csv/user_events"
LOG_FILE = "logs/events_postgres_load.log"

# ---------------- LOGGING ----------------
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_events():
    try:
        ingest_date = datetime.now().strftime("%Y-%m-%d")
        csv_path = f"{BASE_RAW_PATH}/ingest_date={ingest_date}/user_events.csv"

        df = pd.read_csv(csv_path)
        logging.info(f"Rows to insert: {len(df)}")

        engine = create_engine(
            f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

        with engine.begin() as conn:
            df.to_sql(TABLE_NAME, conn, if_exists="append", index=False)

        logging.info("User events loaded into PostgreSQL successfully")

    except Exception as e:
        logging.error(f"User events PostgreSQL load failed: {str(e)}")
        raise

if __name__ == "__main__":
    load_events()
