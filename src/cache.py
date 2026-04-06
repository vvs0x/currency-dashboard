import os
import json
import time
from src.fetch_data import FetchData

class Cache(FetchData):
    def __init__(self, url:str, retries:int = 5, timeout_seconds=600, cache_file='cache.json'):
        super().__init__(url, retries)
        self._timeout_seconds = timeout_seconds
        self._cache_file = cache_file

    def _is_cache_valid(self) -> bool:
        if not os.path.exists(self._cache_file):
            return False
        file_age = time.time() - os.stat(self._cache_file).st_mtime
        return file_age < self._timeout_seconds

    def get(self) -> dict:
        if self._is_cache_valid():
            with open(self._cache_file, 'r') as f:
                return json.load(f)
        data = super().get_data()
        with open(self._cache_file, 'w') as f:
            json.dump(data, f)
        return data