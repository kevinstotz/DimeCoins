from DimeCoins.models import Xchange, Currency
from DimeCoins.settings.base import XCHANGE
from DimeCoins.classes import Coins
from datetime import datetime, timedelta
import logging
import time
import requests

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',
                    )


class CoinDesk:

    def __init__(self, xchange=XCHANGE['COINDESK'], comparison_currency='USD'):
        #  instance variable unique to each instance
        self.xchange = Xchange.objects.get(pk=xchange)
        self.comparison_currency = comparison_currency

    def get(self):
        start_date = datetime.date(datetime.utcnow())
        end_date = start_date - timedelta(days=600)

        currencies = Currency.objects.all()
        # while end_date < start_date:
        for currency in currencies:
            if currency.symbol != 'BTC':
                continue

            prices = self.getPrice(currency.symbol, end_date=start_date, start_date=end_date)
            coins = Coins.Coins()
            if prices == 0 or prices == 'NoneType' or prices == []:
                print(currency.symbol + "Not found")
                continue

            for key in prices['bpi']:
                coin = coins.get_coin_type(symbol=currency.symbol, time=int(time.mktime(start_date.timetuple())), exchange=self.xchange)
                coin.time = int(time.mktime(start_date.timetuple()))
                coin.close = prices['bpi'][key]
                coin.xchange = self.xchange
                coin.currency = currency
                coin.save()
         #   start_date = start_date - timedelta(days=1)

    def getPrice(self, currency_symbol, start_date=datetime.utcnow(), end_date=datetime.utcnow(), granularity=86400):

        headers = {'content-type': 'application/json','user-agent': 'your-own-user-agent/0.0.1'}
        params = {
                  'index': self.comparison_currency,
                  'currency': currency_symbol,
                  'start': start_date,
                  'end': end_date}

        spot_price = requests.get(self.xchange.api_url + '/bpi/historical/close.json', params=params, headers=headers)
        print(spot_price.url)
        if spot_price.status_code == requests.codes.ok:
            return spot_price.json()
        else:
            return([])
