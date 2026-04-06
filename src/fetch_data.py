import urllib.request as ur
from urllib.error import HTTPError, URLError
import json
import time
import ssl

class FetchData:
    def __init__(self, url:str, retries:int = 5):
        self._url = url
        self._retries = retries
        self._response = None
        self._data = None

    def get_data(self) -> dict:
        ctx = ssl._create_unverified_context()
        for attempt in range(self._retries):
            try:
                self._response = ur.urlopen(self._url, context=ctx)
                self._data = json.loads(self._response.read().decode())
                return self._data
            except HTTPError as e:
                print(f'HTTP error {e.code}: {e.reason}')
            except URLError as e:
                print(f'Connection failed: {e.reason}')
            except Exception as e:
                print(f'Unexpected error: {e}')
            wait = 2 ** attempt
            time.sleep(wait)
        raise ValueError(f'Max retries exceeded.')