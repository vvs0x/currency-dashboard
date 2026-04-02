from src.fetch_data import FetchData
import pandas as pd

if __name__ == '__main__':
    url = 'https://data.snb.ch/api/cube/devkua/data/json/de'
    c = FetchData(url=url, retries=5)
    data = c.get_data()
    print(data)
    df = pd.DataFrame(data)
