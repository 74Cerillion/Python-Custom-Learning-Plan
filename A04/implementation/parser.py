import json
import logging
from datetime import datetime
from typing import Any, Dict
from models import MarketObservation, IngestionContext

logger = logging.getLogger(__name__)


class MarketDataParser:
    def parse(self, raw_json: str, context: IngestionContext) -> MarketObservation:
        """Parses raw JSON string into a MarketObservation domain object."""
        logger.info("[%s] Parsing raw market payload...", context.correlation_id)

        try:
            data: Dict[str, Any] = json.loads(raw_json)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON format: {exc}") from exc

        # Required field validations
        required_fields = {"symbol", "price", "timestamp"}
        missing = required_fields - set(data.keys())
        if missing:
            raise ValueError(f"Missing required payload key(s): {sorted(list(missing))}")

        # Field-level validations
        symbol = str(data["symbol"]).upper()
        
        try:
            price = float(data["price"])
            if price <= 0:
                raise ValueError("Price must be greater than 0")
        except (ValueError, TypeError) as exc:
            raise ValueError(f"Invalid price value '{data['price']}': {exc}") from exc

        try:
            timestamp = datetime.fromisoformat(data["timestamp"])
        except (ValueError, TypeError) as exc:
            raise ValueError(f"Invalid ISO timestamp format '{data['timestamp']}': {exc}") from exc

        return MarketObservation(
            symbol=symbol,
            price=price,
            timestamp=timestamp
        )