from DimeCoins.models import Xchange, Currency
from DimeCoins.classes import Coins
from coinbase.wallet.client import Client
import coinbase
from django.core.exceptions import ObjectDoesNotExist
from DimeCoins.settings.base import XCHANGE
from datetime import datetime, timedelta
import logging
import time

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',
                    )


class Coinbase:

    def __init__(self, xchange_id=XCHANGE['COINBASE'], comparison_currency='USD'):
        #  instance variable unique to each instance
        self.xchange = Xchange.objects.get(pk=xchange_id)
        try:
            self.client = Client(self.xchange.api_key, self.xchange.api_secret)
        except ObjectDoesNotExist as error:
            logging.debug('Client does not exist:{0}'.format( error))
        self.comparison_currency = comparison_currency
        self.coin_list_url = 'https://www.cryptocompare.com/api/data/coinlist/'

    def __date_to_iso8601(self, date_time):
        return '{year}-{month:02d}-{day:02d}'.format(
            year=date_time.tm_year,
            month=date_time.tm_mon,
            day=date_time.tm_mday)

    def get(self):
        i=0
        start_date = datetime.date(datetime.utcnow())
        end_date = start_date - timedelta(days=700)
        while end_date < start_date:
            currencies = Currency.objects.all()
            for currency in currencies:
                price = self.getPrice(currency.symbol, date=start_date)
                if price == 0:
                    continue
                coins = Coins.Coins()
                if price == {}:
                    print(currency.symbol + "Not found")
                    continue
                coin = coins.get_coin_type(symbol=currency.symbol, time=int(time.mktime(start_date.timetuple())), exchange=self.xchange)
                coin.time = int(time.mktime(start_date.timetuple()))
                coin.close = float(price.amount)
                coin.xchange = self.xchange
                coin.currency = currency
                coin.save()
            start_date = start_date - timedelta(days=1)

    def getPrice(self, currency_symbol, date):
        try:
            res = self.client.get_spot_price(currency_pair=currency_symbol + '-USD', date=date)
        except:
           res = 0
        return res