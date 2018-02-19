from DimeCoins.models import Xchange, Currency
from DimeCoins.classes import Coins
from django.core.exceptions import ObjectDoesNotExist
from DimeCoins.settings.base import XCHANGE
from datetime import datetime, timedelta
import time

import logging
import requests


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',
                    )


class CoinApi:

    def __init__(self, xchange=XCHANGE['COIN_API'], comparison_currency='USD'):
        #  instance variable unique to each instance

        self.xchange = Xchange.objects.get(pk=xchange)
        self.comparison_currency = comparison_currency

    @staticmethod
    def __date_to_iso8601(date_time):
        return '{year}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}'.format(
            year=date_time.year,
            month=date_time.month,
            day=date_time.day,
            hour=date_time.hour,
            minute=date_time.minute,
            second=date_time.second)

    def get(self):
        i=0
        start_date = datetime.date(datetime.utcnow())
        end_date = start_date - timedelta(days=2)
        while end_date < start_date:
            currencies = Currency.objects.all()
            for currency in currencies:
                prices = self.getPrice(currency.symbol, start_date=start_date, end_date=end_date)

                coins = Coins.Coins()
                if prices == 0 or prices == 'NoneType' or prices == []:
                    print(currency.symbol + "Not found")
                    continue
                for price in prices:
                    print(price)
                    if price == {}:
                        print(currency.symbol + "Not found")
                        continue
                    coin = coins.get_coin_type(symbol=currency.symbol, time=int(time.mktime(start_date.timetuple())), exchange=self.xchange)
                    coin.time = int(time.mktime(start_date.timetuple()))
                    coin.open = float(price['price_open'])
                    coin.close = float(price['price_close'])
                    coin.high = float(price['price_high'])
                    coin.low = float(price['price_low'])
                    coin.xchange = self.xchange
                    coin.currency = currency
                    coin.save()
            start_date = start_date - timedelta(days=1)

    def getPrice(self, currency_symbol, start_date, end_date, limit=300, period_id='1DAY'):
        headers = {'content-type': 'application/json',
                   'user-agent': 'your-own-user-agent/0.0.1',
                   'X-CoinAPI-Key': self.xchange.api_key}
        params = {
                  'period_id': period_id,
                  'time_start': start_date,
                  'limit': limit,
                  'time_end': end_date}
        #spot_price = requests.get(self.xchange.api_url + '/ohlcv/' + currency_symbol + '/history', params=params, headers=headers)
        spot_price = requests.get(self.xchange.api_url + '/ohlcv/BITSTAMP_SPOT_BTC_USD/history', params=params, headers=headers)

        if spot_price.status_code == requests.codes.ok:
            return spot_price.json()
        else:
            return([])
