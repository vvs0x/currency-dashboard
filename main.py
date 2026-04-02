from src.fetch_data import FetchData

if __name__ == '__main__':
    url = 'https://data.snb.ch/api/cube/devkua/data/json/de'
    c = FetchData(url=url, retries=5)
    data = c.get_data()
    print(data)
    