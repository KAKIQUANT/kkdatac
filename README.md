# kkdatac
Querying data from various databases maintained by kkdatabase

## Tutorial:
### 1. Install the package
```bash
# pip install kkdatac
pip install git+https://github.com/KAKIQUANT/kkdatac.git
```
### 2. Import the package
```python
from kkdatac import get_price, sql
# or just import kkdatac
```
### 3. Use the package
```python
# Simple query
import kkdatac
kkdatac.sql('show tables')
kkdatac.sql('show databases')
```
```python
# Query the financial data
import kkdatac
# Query balancesheet
# TODO: Add more examples
```

### Examining the database
```bash
python test/db_report.py
```