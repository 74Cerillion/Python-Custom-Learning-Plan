import logging
from models import MarketObservation, IngestionContext
from parser import MarketDataParser
from repository import MarketDataRepository

logger = logging.getLogger(__name__)


class IngestionOrchestrator:
    def __init__(self, parser: MarketDataParser, repository: MarketDataRepository):
        self.parser = parser
        self.repository = repository

    def process(self, raw_payload: str, context: IngestionContext) -> bool:
        """Coordinates the end-to-end ingestion flow for a single payload."""
        logger.info("[%s] Beginning ingestion pipeline", context.correlation_id)

        try:
            # Step 1: Parse & Validate payload
            observation: MarketObservation = self.parser.parse(raw_payload, context)

            # Step 2: Persist Domain Object
            record_id = self.repository.save(observation, context)

            logger.info(
                "[%s] Successfully ingested observation for %s (Record ID: %d)",
                context.correlation_id,
                observation.symbol,
                record_id
            )
            return True

        except Exception as exc:
            # Application boundary safety: Catch and log without dumping sensitive context payloads
            logger.error(
                "[%s] Ingestion failed: %s",
                context.correlation_id,
                str(exc)
            )
            return False