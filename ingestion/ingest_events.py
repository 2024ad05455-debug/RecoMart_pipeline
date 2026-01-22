import pandas as pd
import logging
import os
from datetime import datetime

# ---------------- CONFIG ----------------
RAW_CSV_SOURCE = "data/raw/csv/sample_events_2000.csv"   # original source
BASE_RAW_PATH = "data/raw/csv/user_events"
LOG_FILE = "logs/ingestion_events.log"

EXPECTED_COLUMNS = [
    "event_time", "event_type", "product_id", "category_id",
    "category_code", "brand", "price", "user_id", "user_session"
]

# ---------------- LOGGING ----------------
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------------- INGEST ----------------
def ingest_events():
    try:
        logging.info("User events ingestion started")

        df = pd.read_csv(RAW_CSV_SOURCE)

        # Schema validation
        if not set(EXPECTED_COLUMNS).issubset(df.columns):
            raise ValueError("CSV schema mismatch")

        # Basic cleaning
        df["event_time"] = pd.to_datetime(df["event_time"], errors="coerce")
        df = df.dropna(subset=["event_time", "event_type", "product_id", "user_id"])

        ingest_date = datetime.now().strftime("%Y-%m-%d")
        raw_path = os.path.join(BASE_RAW_PATH, f"ingest_date={ingest_date}")
        os.makedirs(raw_path, exist_ok=True)

        output_file = os.path.join(raw_path, "user_events.csv")
        df.to_csv(output_file, index=False)

        logging.info(
            f"User events ingestion successful | Records: {len(df)} | Path: {output_file}"
        )

    except Exception as e:
        logging.error(f"User events ingestion failed: {str(e)}")
        raise

if __name__ == "__main__":
    ingest_events()
