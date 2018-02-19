from DimeCoins.models import Xchange, Currency
from DimeCoins.classes import Coins
from DimeCoins.settings.base import XCHANGE
from datetime import datetime, timedelta
import logging
import requests


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',
                    )


class Gdax:

    def __init__(self, xchange=XCHANGE['GDAX'], comparison_currency='USD', granularity=86400):
        #  instance variable unique to each instance

        self.xchange = Xchange.objects.get(pk=xchange)
        self.comparison_currency = comparison_currency
        self.granularity = granularity  #  per day
        self.xx = '/products/{pair}/candles?granularity=86400&start=2017-01-17T00:00:00&end=2017-02-17T00:00:00'.format(pair="BTC-USD")

    def __date_to_iso8601(self, date_time):
        return '{year}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}'.format(
            year=date_time.tm_year,
            month=date_time.tm_mon,
            day=date_time.tm_mday,
            hour=date_time.tm_hour,
            minute=date_time.tm_min,
            second=date_time.tm_sec)

    def get(self):
        start = datetime.utcnow() - timedelta(days=3)
        start = start.timetuple()
        end = datetime.utcnow().timetuple()
        currencies = Currency.objects.all()
        for currency in currencies:
            prices = self.getPrice(currency.symbol, start_date=self.__date_to_iso8601(date_time=start), end_date=self.__date_to_iso8601(date_time=end))
            coins = Coins.Coins()
            if prices == 0 or prices == 'NoneType' or prices == []:
                print(currency.symbol + "Not found")
                continue
            for price in prices:
                coin = coins.get_coin_type(symbol=currency.symbol, time=int(price[0]), exchange=self.xchange)
                coin.time = int(price[0])
                coin.low = float(price[1])
                coin.high = float(price[2])
                coin.open = float(price[3])
                coin.close = float(price[4])
                coin.xchange = self.xchange
                coin.currency = currency
                coin.save()

    def getPrice(self, currency_symbol, start_date=datetime.utcnow(), end_date=datetime.utcnow(), granularity=86400):

        headers = {'content-type': 'application/json','user-agent': 'your-own-user-agent/0.0.1'}
        spot_price = requests.get(self.xchange.api_url + '/products/' + currency_symbol + '-' +
                                  self.comparison_currency + '/candles?granularity={0}&start={1}&end={2}'.format(granularity, start_date, end_date), headers=headers)
        if spot_price.status_code == requests.codes.ok:
            return spot_price.json()
        else:
            return([])
