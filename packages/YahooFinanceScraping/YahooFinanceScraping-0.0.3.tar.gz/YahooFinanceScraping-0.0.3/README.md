# YahooFinanceScraping

**YahooFinanceScraping** is a library to scraping quote data.

## Features

- Regular market price.
- Previous close.
- Open value.
- Days range.

## Installation

- Run `pip install yahoofinancescraping`

## Example

```python
from yfs import YahooFinanceScraping

yfs = YahooFinanceScraping('IBM')

regular_market_price = yfs.regular_market_price()
print(regular_market_price)

previous_close = yfs.previous_close()
print(previous_close)

open_value = yfs.open_value()
print(open_value)

days_range = yfs.days_range()
print(days_range)

```

### Console Output

```bash
foo@bar ~/
$ python test.py
133,04
132,21
133,00
{'min': Decimal('130.89'), 'max': Decimal('133.77')}
```

## Upgrade

- Run `pip install yahoofinancescraping --upgrade`
