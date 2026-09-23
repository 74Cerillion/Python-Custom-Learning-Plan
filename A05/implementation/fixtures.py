from dataclasses import dataclass

@dataclass
class Fixture:
    symbol: str
    delay: float
    should_timeout: bool = False

# Controlled market-data fixtures
FIXTURES = [
    Fixture("AAPL", 0.1),                # Fast I/O
    Fixture("MSFT", 0.3),                # Medium I/O
    Fixture("NVDA", 0.2),                # Fast I/O
    Fixture("AMD",  0.5),                # Slow I/O
    Fixture("GOOG", 2.0, should_timeout=True), # Will simulate a network timeout
]