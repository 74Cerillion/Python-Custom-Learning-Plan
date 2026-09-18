test = {
    "symbol": "AAPL",
    "price": 234.56,
    "timestamp": "2026-09-16T09:31:00"
}

from datetime import datetime

def _validate(ni):
    if not str(ni["symbol"]):
        return "Invalid Stock"
    if not float(ni["price"]):
        return "Invalid Price"
    try:
        ni['timestamp'] = datetime.fromisoformat(ni["timestamp"])
    except:
        return "Invalid Timestamp"

    return ni

def format(ni):
    toFormat = _validate(ni)
    try:
        return ("{}: ${}. Price Obtained: {}".format(toFormat["symbol"],
                                                   toFormat["price"],
                                                   toFormat["timestamp"]))
    except:
        return "Invalid Structure"

output = format(test)
print(output)