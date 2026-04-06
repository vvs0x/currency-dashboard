import matplotlib.pyplot as plt
import pandas as pd
from src.cache import Cache
from src.currency_stats import parse_data, shorten_currency

url = 'https://data.snb.ch/api/cube/devkum/data/json/de'
cache = Cache(url=url, retries=5, timeout_seconds=600)
data = cache.get()

df = parse_data(data)
df["currency"] = df["currency"].apply(shorten_currency)
df["value"] = pd.to_numeric(df["value"], errors="coerce")
df["date"] = pd.to_datetime(df["date"])

important = ['EUR', 'USD', 'CNY', 'JPY', 'GBP']
df = df[df["currency"].isin(important)]

print(df.head())  


pivot = df.pivot_table(index="date", columns="currency", values="value")
print(pivot.head())

pivot.plot(figsize=(12, 5), title="Wechselkurse in CHF über die Zeit")
plt.show()

print(df[df["currency"] == "GBP"].tail(20))
print(df[df["currency"] == "GBP"]["value"].dtype)
print(df[df["currency"] == "GBP"]["value"].isna().sum())

gbp = df[df["currency"] == "GBP"]
print(gbp[gbp["date"] >= "1965-01-01"].head(20))

corr = pivot[['EUR', 'USD', 'CNY', 'GBP', 'JPY']].corr()
print(corr)

fig, ax = plt.subplots(figsize=(6, 4))


im = ax.imshow(corr.values, cmap="coolwarm", vmin=-1, vmax=1)


ax.set_xticks(range(len(corr.columns)))
ax.set_yticks(range(len(corr.columns)))
ax.set_xticklabels(corr.columns)
ax.set_yticklabels(corr.columns)


for i in range(len(corr)):
    for j in range(len(corr.columns)):
        ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center")

plt.colorbar(im, ax=ax)
plt.title("Korrelation EUR, USD, CNY")
plt.tight_layout()
plt.show()


fig, axes = plt.subplots(1, 5, figsize=(18, 4))

for ax, currency in zip(axes, important):
    subset = df[df["currency"] == currency]["value"]
    subset.plot(kind="hist", bins=30, ax=ax, title=currency)
    ax.set_xlabel("Kurs (CHF)")

plt.suptitle("Verteilung der Wechselkurswerte")
plt.tight_layout()
plt.show()