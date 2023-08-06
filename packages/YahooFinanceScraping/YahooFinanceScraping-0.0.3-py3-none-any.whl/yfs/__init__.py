""" docstring """


import requests
from decimal import Decimal
from bs4 import BeautifulSoup


__version__ = '0.0.3'


class YahooFinanceScraping():
    """ docstring """

    def __init__(self, symbol, user_agent='Mozilla/5.0'):
        """ docstring """

        self.symbol = symbol
        self.user_agent = user_agent
        self.request = None
        self.page = None

        self.execute()

    def execute(self):
        """ docstring """

        headers={'User-agent': self.user_agent,}

        self.request = requests.get(
            f"https://br.financas.yahoo.com/quote/{self.symbol}/",
            headers=headers
        )

        self.page = BeautifulSoup(self.request.content, 'html.parser')


    def value_to_decimal(self, value):
        value = value.replace(',', '.')
        value = Decimal(value)
        return value


    def regular_market_price(self):    
        value = self.page.find('fin-streamer', attrs={'data-symbol': f'{self.symbol}', 'data-field': 'regularMarketPrice'}).text
        return self.value_to_decimal(value)


    def previous_close(self):
        value = self.page.find('td', attrs={'data-test': 'PREV_CLOSE-value'}).text
        return self.value_to_decimal(value)


    def open_value(self):
        value = self.page.find('td', attrs={'data-test': 'OPEN-value'}).text
        return self.value_to_decimal(value)


    def days_range(self):
        
        values = self.page.find('td', attrs={'data-test': 'DAYS_RANGE-value'}).text
        values = values.split('-')

        min_value = values[0]
        min_value = min_value.replace(',','.')
        min_value = self.value_to_decimal(min_value)

        max_value = values[1]
        max_value = max_value.replace(',','.')
        max_value = self.value_to_decimal(max_value)

        values = {
            'min': min_value,
            'max': max_value,
        }

        return values
