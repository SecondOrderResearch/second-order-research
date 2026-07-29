import sqlite3
import pandas as pd
from pathlib import Path
from src.config import DB_PATH, DB_URL
from src.logging_config import setup_logging

logger = setup_logging("storage")

class Storage:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        logger.info(f"Connected to SQLite database at {self.db_path}")

    def execute(self, sql: str, params: tuple = ()) -> None:
        try:
            self.conn.execute(sql, params)
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to execute SQL: {sql} | Error: {e}")
            raise

    def execute_many(self, sql: str, params_list: list) -> None:
        try:
            self.conn.executemany(sql, params_list)
            self.conn.commit()
        except Exception as e:
            logger.error(f"Failed to execute many SQL: {sql} | Error: {e}")
            raise

    def fetch_df(self, sql: str, params: tuple = ()) -> pd.DataFrame:
        try:
            return pd.read_sql_query(sql, self.conn, params=params)
        except Exception as e:
            logger.error(f"Failed to fetch DataFrame: {sql} | Error: {e}")
            raise

    def fetch_one(self, sql: str, params: tuple = ()):
        try:
            cursor = self.conn.execute(sql, params)
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Failed to fetch one: {sql} | Error: {e}")
            raise

    def insert_df(self, table: str, df: pd.DataFrame, if_exists: str = "append") -> None:
        try:
            df.to_sql(table, self.conn, if_exists=if_exists, index=False)
            logger.info(f"Inserted {len(df)} rows into {table}")
        except Exception as e:
            logger.error(f"Failed to insert DataFrame into {table}: {e}")
            raise

    def close(self) -> None:
        self.conn.close()
        logger.info("Database connection closed")
