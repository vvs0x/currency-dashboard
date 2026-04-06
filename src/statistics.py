import pandas as pd
from src.cache import Cache
from scipy import stats


def parse_data(raw: dict) -> pd.DataFrame:
    """Converts the raw SNB JSON into a clean table with columns: date, value, currency"""
    frames = []
    for series in raw["timeseries"]:
        currency = series["header"][1]["dimItem"]  # e.g. "Europa - EUR 1.-"
        values = series["values"]                  # list of {date, value}
        df = pd.DataFrame(values)
        df["currency"] = currency
        frames.append(df)
    return pd.concat(frames, ignore_index=True)


def shorten_currency(name: str) -> str:
    """Shortens long currency names to 3-letter codes."""
    mapping = {
        'Europa - EUR 1.-': 'EUR',
        'Amerika - USA – USD 1.-': 'USD',
        'Asien und Australien - China – CNY 100.-': 'CNY',
        'Asien und Australien - Japan – JPY 100.-': 'JPY',
        'Europa - Vereinigtes Königreich – GBP 1.-': 'GBP',
    }
    return mapping.get(name, name)


def calculate_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates key statistics for each currency"""
    results = []
    for currency, group in df.groupby("currency"):
        v = group["value"]
        results.append({
            "currency": currency,
            "mean":     round(v.mean(), 4),   # average exchange rate
            "variance": round(v.var(), 4),    # how much the values spread
            "std":      round(v.std(), 4),    # standard deviation
            "skewness": round(stats.skew(v), 4),      # is the distribution tilted?
            "kurtosis": round(stats.kurtosis(v), 4),  # are there extreme outliers?
        })
    return pd.DataFrame(results)


def print_statistics(stats_df: pd.DataFrame):
    """Prints the statistics table with borders"""
    header = f"{'Currency':<8} | {'Mean':>8} | {'Variance':>10} | {'Std':>8} | {'Skewness':>10} | {'Kurtosis':>10}"
    line   = "-"*8 + "+" + "-"*10 + "+" + "-"*12 + "+" + "-"*10 + "+" + "-"*12 + "+" + "-"*12
    print(header)
    print(line)
    for _, row in stats_df.iterrows():
        print(f"{row['currency']:<8} | {row['mean']:>8.4f} | {row['variance']:>10.4f} | {row['std']:>8.4f} | {row['skewness']:>10.4f} | {row['kurtosis']:>10.4f}")
    print("=" * len(header))


def print_correlation(corr: pd.DataFrame):
    """Prints the correlation matrix  values close to 1 mean currencies move together """
    currencies = corr.columns.tolist()
    header = f"{'':>6} | " + " | ".join(f"{c:>8}" for c in currencies)
    line   = "-"*6 + "+" + ("----------+" * len(currencies))
    print(header)
    print(line)
    for currency, row in corr.iterrows():
        values = " | ".join(f"{row[c]:>8.4f}" for c in currencies)
        print(f"{currency:>6} | {values}")
    print("=" * len(header))


if __name__ == '__main__':
    url = 'https://data.snb.ch/api/cube/devkum/data/json/de'

    # Load data (cached for 10 minutes)
    cache = Cache(url=url, retries=5, timeout_seconds=600)
    data = cache.get()

    # Parse and shorten currency names
    df = parse_data(data)
    df["currency"] = df["currency"].apply(shorten_currency)

    # Filter to most important currencies
    important = ['EUR', 'USD', 'CNY', 'JPY', 'GBP']
    df = df[df["currency"].isin(important)]

    # Print statistics
    print("\nStatistics of major currencies (in CHF):\n")
    print_statistics(calculate_statistics(df))

    # Print correlation between EUR, USD and CNY
    pivot = df.groupby(["date", "currency"])["value"].mean().unstack()
    corr = pivot[['EUR', 'USD', 'CNY']].corr()
    print("\n Correlation between EUR, USD and CNY:\n")
    print_correlation(corr)