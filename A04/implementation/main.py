import logging
import uuid
from models import IngestionContext
from parser import MarketDataParser
from repository import MarketDataRepository
from orchestrator import IngestionOrchestrator

# Setup visible stdout logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger("main")


def main():
    logger.info("Initializing Ingestion Infrastructure...")

    # Wire component hierarchy (Dependency Injection)
    parser = MarketDataParser()
    repository = MarketDataRepository(db_path=":memory:")
    orchestrator = IngestionOrchestrator(parser=parser, repository=repository)

    # -------------------------------------------------------------------
    # DEMO 1: Valid Path Execution
    # -------------------------------------------------------------------
    print("\n--- RUNNING VALID PATH DEMO ---")
    valid_payload = """
    {
        "symbol": "AAPL",
        "price": 234.56,
        "timestamp": "2026-09-21T09:31:00"
    }
    """
    valid_context = IngestionContext(
        correlation_id=f"corr-{uuid.uuid4().hex[:8]}",
        api_key="SUPER_SECRET_BLAH_BLAH"
    )

    success = orchestrator.process(valid_payload, valid_context)
    
    # Verification of DB State
    if success:
        persisted = repository.get_latest_by_symbol("AAPL")
        print(f"[VERIFICATION] Database query retrieved row: {persisted}")

    # -------------------------------------------------------------------
    # DEMO 2: Intentional Failure Path (Malformed Payload)
    # -------------------------------------------------------------------
    print("\n--- RUNNING FAILURE PATH DEMO ---")
    invalid_payload = """
    {
        "symbol": "AAPL",
        "price": "INVALID_PRICE_VALUE",
        "timestamp": "2026-09-21T09:31:00"
    }
    """
    failure_context = IngestionContext(
        correlation_id=f"corr-{uuid.uuid4().hex[:8]}",
        api_key="SUPER_SECRET_BLAH_BLAH"
    )

    # Triggering failure path
    orchestrator.process(invalid_payload, failure_context)


if __name__ == "__main__":
    main()