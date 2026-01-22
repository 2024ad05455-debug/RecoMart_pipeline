import requests
import json
import logging
import os
import time
from datetime import datetime

API_URL = "https://dummyjson.com/products"
MAX_RETRIES = 3
BASE_RAW_PATH = "data/raw/api/product_data"
LOG_FILE = "logs/ingestion_products_api.log"

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def ingest_products():
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logging.info(f"API ingestion attempt {attempt}")
            response = requests.get(API_URL, timeout=10)
            response.raise_for_status()

            data = response.json()

            ingest_date = datetime.now().strftime("%Y-%m-%d")
            raw_path = os.path.join(BASE_RAW_PATH, f"ingest_date={ingest_date}")
            os.makedirs(raw_path, exist_ok=True)

            output_file = os.path.join(raw_path, "products.json")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            logging.info(
                f"Product API ingestion successful | Products: {len(data['products'])}"
            )
            return

        except Exception as e:
            logging.error(f"Attempt {attempt} failed: {str(e)}")
            time.sleep(5)

    logging.critical("Product API ingestion failed after retries")

if __name__ == "__main__":
    ingest_products()
