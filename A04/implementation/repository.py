import sqlite3
import logging
from typing import Optional
from models import MarketObservation, IngestionContext

logger = logging.getLogger(__name__)


class MarketDataRepository:
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS market_observations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    price REAL NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)
            conn.commit()

    def save(self, observation: MarketObservation, context: IngestionContext) -> int:
        """Persists a MarketObservation and returns inserted row ID."""
        logger.info(
            "[%s] Persisting observation for symbol %s to DB...",
            context.correlation_id,
            observation.symbol
        )
        sql = """
            INSERT INTO market_observations (symbol, price, timestamp)
            VALUES (?, ?, ?)
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                sql,
                (observation.symbol, observation.price, observation.timestamp.isoformat())
            )
            conn.commit()
            return cursor.lastrowid

    def get_latest_by_symbol(self, symbol: str) -> Optional[MarketObservation]:
        """Utility method to verify database persistence state."""
        sql = """
            SELECT symbol, price, timestamp
            FROM market_observations
            WHERE symbol = ?
            ORDER BY id DESC LIMIT 1
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (symbol.upper(),))
            row = cursor.fetchone()
            if not row:
                return None
            return MarketObservation(
                symbol=row[0],
                price=row[1],
                timestamp=datetime.fromisoformat(row[2])
            )