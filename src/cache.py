import time
from src.fetch_data import FetchData

class Cache(FetchData):
    def __init__(self, url:str, retries:int = 5, timeout_seconds=600):
        super().__init__(url, retries)
        self._cached_data = None
        self._last_fetch_time = 0
        self._timeout_seconds = timeout_seconds

    def get(self) -> dict:
        current_time = time.time()
        if self._cached_data is None or (current_time - self._last_fetch_time) >= self._timeout_seconds:
            self._cached_data = super().get_data() 
            self._last_fetch_time = current_time
        return self._cached_data