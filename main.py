from src.cache import Cache
import pandas as pd
import time

if __name__ == '__main__':
    url = 'https://data.snb.ch/api/cube/devkum/data/json/de'

    # Create cache with 10 minute timeout
    cache = Cache(url=url, retries=5, timeout_seconds=600)

    # First call: fetches from API and caches
    print("First call - fetching from API...")
    data = cache.get()
    print(f"Got {len(data)} records\n")
    df = pd.DataFrame(data)

    # Second call: returns cached data (no API call)
    print("Second call - returning cached data...")
    data = cache.get()
    print(f"Got {len(data)} records (from cache)\n")
    # After 10 minutes, next call to get() will fetch fresh data
    # Example (uncomment to test):
    # print("Waiting 600+ seconds...")
    # time.sleep(601)
    # print("Third call - fetching fresh data from API...")
    # data = cache.get()
    # print(f"Got {len(data)} records")
