import os
import time
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

# Load env vars
DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASS = os.getenv("DB_PASS", "admin123")
DB_NAME = os.getenv("DB_NAME", "mydb")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
engine = create_engine(DATABASE_URL)


def wait_for_db(engine, retries=10, delay=5):
    
    for i in range(retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                print("Database is ready")
                return
        except OperationalError:
            print(f"Database not ready, retrying in {delay} sec... ({i+1}/{retries})")
            time.sleep(delay)

    raise Exception("Database not ready after retries")

def load_csv_to_db(file_path, table_name, pk_column):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    print(f"Loading {file_path} into {table_name}...")
    df = pd.read_csv(file_path)

    # Drop existing table
    with engine.connect() as conn:
        conn.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE;"))
        conn.commit()

    # Create without constraints
    df.head(0).to_sql(table_name, engine, if_exists="replace", index=False)

    # Add PK
    with engine.connect() as conn:
        conn.execute(text(f"ALTER TABLE {table_name} ADD PRIMARY KEY ({pk_column});"))
        conn.commit()

    # Insert data
    df.to_sql(table_name, engine, if_exists="append", index=False)
    print(f"Loaded {len(df)} rows into {table_name}")


wait_for_db(engine)  

# Load datasets
load_csv_to_db("./data/tmdb_5000_movies1.csv", "movie_metadata", "id")
load_csv_to_db("./data/tmdb_5000_movies2.csv", "movie_details", "id")
load_csv_to_db("./data/tmdb_5000_movies3.csv", "movie_castcrew", "movie_id")

with engine.connect() as conn:
    print("\n Top 5 movies by revenue:")
    result = conn.execute(text("""
        SELECT m.original_title, d.revenue
        FROM movie_details d
        JOIN movie_metadata m ON d.id = m.id
        ORDER BY d.revenue DESC
        LIMIT 5;
    """))
    for row in result:
        print(row)

    print("\n Top 5 movies by average rating (with at least 1000 votes):")
    result = conn.execute(text("""
        SELECT m.original_title, d.vote_average, d.vote_count
        FROM movie_details d
        JOIN movie_metadata m ON d.id = m.id
        WHERE d.vote_count > 1000
        ORDER BY d.vote_average DESC
        LIMIT 5;
    """))
    for row in result:
        print(row)


    print("\n Inserting a test movie...")
    conn.execute(text("""
        INSERT INTO movie_metadata (id, budget, homepage, original_language, original_title)
        VALUES (9999999, 100000, 'http://test.com', 'en', 'Test Movie')
        ON CONFLICT (id) DO NOTHING;
    """))
    conn.commit()
    print(" Insert complete")

    print("\n Example 3-table join (metadata + details + castcrew):")
    result = conn.execute(text("""
        SELECT m.original_title, d.release_date, d.vote_average, c.tagline
        FROM movie_metadata m
        JOIN movie_details d ON m.id = d.id
        JOIN movie_castcrew c ON m.id = c.movie_id
        LIMIT 5;
    """))
    for row in result:
        print(row)
