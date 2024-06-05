# kkdatac
Querying data from various databases maintained by kkdatabase

## Tutorial:
### 1. Install the package
```bash
pip install kkdatac
```
### 2. Import the package
```python
from kkdatac import get_price
```
### 3. Use the package
```python
# For OKX_CRYPTO
df = get_price(
    "BTC-USDT-SWAP",
    start_date="2023-01-01",
    end_date="2024-01-01",
    frequency="1D",
    fields=["open", "high", "low", "close"],
    adjust_type="pre",
    skip_suspended=False,
    market="crypto",
    expect_df=True,
    time_slice=None,
)

print(df)
```
OR, for CN_STOCK
```python
df = get_price(
    "000001",
    "2013-01-04",
    "2014-01-04",
    "1D",
    None,
    "pre",
    False,
    "cn_stock",
    True,
    None,
)
print(df)
df.plot(x="datetime", y="close")
plt.show()
```