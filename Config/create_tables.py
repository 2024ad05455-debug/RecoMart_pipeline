from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# -------------------------------
# Database Configuration
# -------------------------------
DB_USER = "postgres"
DB_PASSWORD = "postgres"     # change if required
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "RecoMart_DB"

# -------------------------------
# Create Database (if not exists)
# -------------------------------
def create_database():
    try:
        engine = create_engine(
            f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres",
            isolation_level="AUTOCOMMIT"
        )

        with engine.connect() as conn:
            conn.execute(
                text(f'CREATE DATABASE "{DB_NAME}"')
            )
            print(f"Database {DB_NAME} created successfully")

    except OperationalError:
        print(f"Database {DB_NAME} already exists")
    except Exception as e:
        print("Error creating database:", e)

# -------------------------------
# Create Tables
# -------------------------------
def create_tables():
    engine = create_engine(
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    create_events_table = """
    CREATE TABLE IF NOT EXISTS ecommerce_events (
        event_time TIMESTAMP,
        event_type VARCHAR(20),
        product_id BIGINT,
        category_id BIGINT,
        category_code VARCHAR(255),
        brand VARCHAR(100),
        price NUMERIC(10,2),
        user_id BIGINT,
        user_session UUID
    );
    """

    create_products_table = """
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        title TEXT,
        brand TEXT,
        category TEXT,
        price NUMERIC(10,2),
        rating NUMERIC(3,2),
        stock INTEGER
    );
    """

    with engine.begin() as conn:
        conn.execute(text(create_events_table))
        conn.execute(text(create_products_table))

    print("Tables ecommerce_events and products created successfully")

# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":
    create_database()
    create_tables()
