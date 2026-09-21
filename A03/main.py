from datetime import datetime
import os
import sqlite3
from typing import Any, Dict, List, Optional, Tuple


class MarketRepository:

    def __init__(self, db_path: str = "market_data.db") -> None:
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        # Enforce SQLite foreign key constraints and type converters if needed
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        """Initialize database schema with a UNIQUE constraint on (symbol, timestamp)."""
        with self._get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS market_observations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    price REAL NOT NULL,
                    timestamp TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(symbol, timestamp)
                )
            """
            )

    def store_observation(self, observation: Dict[str, Any]) -> bool:
        """Stores a single observation safely using parameterized SQL.

        Returns True if inserted, False if ignored due to duplicate (idempotent).
        """
        sql = """
            INSERT OR IGNORE INTO market_observations (symbol, price, timestamp)
            VALUES (?, ?, ?)
        """
        params = (
            observation["symbol"],
            float(observation["price"]),
            observation["timestamp"],
        )

        with self._get_connection() as conn:
            cursor = conn.execute(sql, params)
            # cursor.rowcount will be 1 if inserted, 0 if ignored due to UNIQUE constraint
            return cursor.rowcount > 0

    def store_batch_transactional(
        self, observations: List[Dict[str, Any]], force_failure: bool = False
    ) -> None:
        """Demonstrates atomicity: if any step fails, the entire transaction rolls back."""
        sql = """
            INSERT INTO market_observations (symbol, price, timestamp)
            VALUES (?, ?, ?)
        """
        conn = self._get_connection()
        try:
            with conn:  # Context manager automatically handles BEGIN / COMMIT / ROLLBACK
                for obs in observations:
                    conn.execute(
                        sql, (obs["symbol"], float(obs["price"]), obs["timestamp"])
                    )

                if force_failure:
                    raise RuntimeError("Simulated transaction failure!")
        finally:
            conn.close()

    def retrieve_observation(
        self, symbol: str, timestamp: str
    ) -> Optional[Dict[str, Any]]:
        """Retrieves a single observation by symbol and timestamp using parameterized SQL."""
        sql = """
            SELECT symbol, price, timestamp
            FROM market_observations
            WHERE symbol = ? AND timestamp = ?
        """
        with self._get_connection() as conn:
            row = conn.execute(sql, (symbol, timestamp)).fetchone()
            if row:
                return dict(row)
            return None


# =====================================================================
# Verification & Behavioral Demonstrations
# =====================================================================
if __name__ == "__main__":
    db_filename = "market_repo_demo.db"

    # Clean up prior runs if existing
    if os.path.exists(db_filename):
        os.remove(db_filename)

    print("--- 1. Initialization & Initial Insertion ---")
    repo = MarketRepository(db_path=db_filename)

    sample_obs = {
        "symbol": "AAPL",
        "price": 234.56,
        "timestamp": "2026-09-20T09:31:00",
    }

    inserted = repo.store_observation(sample_obs)
    print(f"Stored AAPL observation: {inserted}")  # True

    retrieved = repo.retrieve_observation(
        "AAPL", "2026-09-20T09:31:00"
    )
    print(f"Retrieved observation:  {retrieved}\n")

    print("--- 2. Uniqueness & Idempotency ---")
    # Attempting to re-insert the identical observation (same symbol + timestamp)
    inserted_again = repo.store_observation(sample_obs)
    print(
        f"Re-inserted identical observation (Expected: False): {inserted_again}\n"
    )

    print("--- 3. Transaction Rollback Demonstration ---")
    batch_data = [
        {"symbol": "MSFT", "price": 420.10, "timestamp": "2026-09-20T09:31:00"},
        {"symbol": "GOOGL", "price": 175.50, "timestamp": "2026-09-20T09:31:00"},
    ]

    try:
        # Pass force_failure=True to raise an error mid-transaction
        repo.store_batch_transactional(batch_data, force_failure=True)
    except RuntimeError as e:
        print(f"Caught intentional error: {e}")

    # Verify MSFT was NOT saved due to rollback
    msft_check = repo.retrieve_observation(
        "MSFT", "2026-09-20T09:31:00"
    )
    print(
        f"MSFT after rolled-back transaction (Expected: None): {msft_check}\n"
    )

    print("--- 4. Persistence across Connection Re-Open ---")
    # Completely destroy the repository instance to force closing open handles
    del repo

    # Re-instantiate repository targeting the same disk file
    new_repo = MarketRepository(db_path=db_filename)
    reopened_read = new_repo.retrieve_observation(
        "AAPL", "2026-09-20T09:31:00"
    )
    print(
        f"Retrieved AAPL from fresh connection: {reopened_read}\n"
    )

    # Clean up generated demo database file
    if os.path.exists(db_filename):
        os.remove(db_filename)