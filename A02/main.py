import json

class MarketDataError(Exception):
    """Custom exception for all adapter-related failures."""
    pass

class MarketDataAdapter:
    def __init__(self, http_client):
        # Injecting the HTTP client makes it trivial to mock controlled responses
        self.http_client = http_client

    def fetch_ticker(self, symbol: str) -> dict:
        """Fetches and parses market data, handling HTTP and JSON errors."""
        try:
            status_code, text_response = self.http_client.get(f"/api/v1/ticker/{symbol}")
        except TimeoutError:
            # 4. Timeout handling
            raise MarketDataError(f"Timeout while fetching data for {symbol}")
        except Exception as e:
            raise MarketDataError(f"Network error: {str(e)}")

        # 2. Non-Success status handling
        if status_code != 200:
            raise MarketDataError(f"Unsuccessful HTTP status: {status_code}")

        # 3. Malformed JSON handling
        try:
            data = json.loads(text_response)
        except json.JSONDecodeError:
            raise MarketDataError("Failed to deserialize response: Malformed JSON")

        # 1. Successful response becomes usable data
        return data


if __name__ == "__main__":
    
    # 1. Successful Response
    class MockSuccessClient:
        def get(self, url):
            return 200, '{"symbol": "AAPL", "price": 234.56, "timestamp": "2026-09-18T10:30:00"}'

    # 2. HTTP Error Status
    class MockErrorStatusClient:
        def get(self, url):
            return 503, '{"error": "Service Unavailable"}'

    # 3. Malformed JSON
    class MockBadJsonClient:
        def get(self, url):
            return 200, '{"symbol": "AAPL", "price": 234.56, "timestamp": ' # Missing closing braces

    # 4. Timeout
    class MockTimeoutClient:
        def get(self, url):
            raise TimeoutError("Connection timed out after 5.0 seconds")


    print("--- 1. Testing Success ---")
    adapter = MarketDataAdapter(MockSuccessClient())
    try:
        data = adapter.fetch_ticker("AAPL")
        print(f"SUCCESS: Usable Python Dictionary -> {data}")
    except MarketDataError as e:
        print(f"FAILED: {e}")

    print("\n--- 2. Testing Non-Success Status ---")
    adapter = MarketDataAdapter(MockErrorStatusClient())
    try:
        adapter.fetch_ticker("AAPL")
    except MarketDataError as e:
        print(f"CAUGHT EXPECTED ERROR: {e}")

    print("\n--- 3. Testing Malformed JSON ---")
    adapter = MarketDataAdapter(MockBadJsonClient())
    try:
        adapter.fetch_ticker("AAPL")
    except MarketDataError as e:
        print(f"CAUGHT EXPECTED ERROR: {e}")

    print("\n--- 4. Testing Timeout ---")
    adapter = MarketDataAdapter(MockTimeoutClient())
    try:
        adapter.fetch_ticker("AAPL")
    except MarketDataError as e:
        print(f"CAUGHT EXPECTED ERROR: {e}")