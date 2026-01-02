# mindatlas/src/load.py
"""
MindAtlas Load Layer

Placeholder for the data loading stage of the pipeline.
Responsible for persisting transformed data into the target storage system
such as DuckDB, cloud storage, or a future data warehouse.

Responsibilities:
- Receive clean transformed dataset
- Load data into DuckDB (planned)
- Provide safe write operations
- Prepare for future optimisation, partitioning and versioning strategies
"""
import duckdb
import logging
from config import DB_PATH, NOTES_TABLE

logging.basicConfig(level=logging.INFO)


def init_db():
    con = duckdb.connect(DB_PATH)

    con.execute(f"""
        CREATE TABLE IF NOT EXISTS {NOTES_TABLE} (
            id TEXT PRIMARY KEY,
            title TEXT,
            created_at TIMESTAMP,
            updated_at TIMESTAMP,
            source_url TEXT,
            body TEXT,
            body_length INTEGER,
            has_source BOOLEAN,
            created_date DATE,
            ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    return con


def load_notes(df):
    if df is None or df.empty:
        logging.warning("No data received. Load skipped.")
        return

    con = init_db()
    con.register("incoming", df)

    logging.info(f"Ingesting {len(df)} records into DuckDB")

    con.execute(f"""
        INSERT INTO {NOTES_TABLE} (
            id,
            title,
            created_at,
            updated_at,
            source_url,
            body,
            body_length,
            has_source,
            created_date
        )
        SELECT
            id,
            title,
            created_at,
            updated_at,
            source_url,
            body,
            body_length,
            has_source,
            CAST(created_date AS DATE)
        FROM incoming
        ON CONFLICT (id) DO UPDATE SET
            title = EXCLUDED.title,
            created_at = EXCLUDED.created_at,
            updated_at = EXCLUDED.updated_at,
            source_url = EXCLUDED.source_url,
            body = EXCLUDED.body,
            body_length = EXCLUDED.body_length,
            has_source = EXCLUDED.has_source,
            created_date = EXCLUDED.created_date;
    """)

    logging.info("Load completed successfully")

