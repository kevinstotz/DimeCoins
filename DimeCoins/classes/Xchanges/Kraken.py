from DimeCoins.models import Xchange, Currency
from DimeCoins.classes import Coins
import krakenex
from django.core.exceptions import ObjectDoesNotExist
from DimeCoins.settings.base import XCHANGE
from datetime import datetime
import logging
from decimal import Decimal

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',
                    )


class Kraken:

    def __init__(self, xchange=XCHANGE['KRAKEN'], comparison_currency='USD'):

        self.since = str(1499000000)  # UTC 2017-07-02 12:53:20
        self.xchange = Xchange.objects.get(pk=xchange)
        try:
            self.kraken = krakenex.API()
        except ObjectDoesNotExist as error:
            logging.debug('Client does not exist:{0}'.format( error))
        self.comparison_currency = comparison_currency


    def __date_to_iso8601(self, date_time):
        return '{year}-{month:02d}-{day:02d}'.format(
            year=date_time.tm_year,
            month=date_time.tm_mon,
            day=date_time.tm_mday)

    def get(self):
        currencies = Currency.objects.all()
        for currency in currencies:
            prices = self.getPrice(currency.symbol)
            if prices == 0:
                continue
            coins = Coins.Coins()
            if prices == {} or prices == None or type(prices) == 'None':
                print(currency.symbol + "Not found")
                continue

            for price in prices:
                coin = coins.get_coin_type(symbol=currency.symbol, time=int(price[0]), exchange=self.xchange)
                coin.time = int(price[0])
                coin.open = float(price[1])
                coin.close = float(price[4])
                coin.high = float(price[2])
                coin.low = float(price[3])
                coin.volume = float(price[6])
                coin.xchange = self.xchange
                coin.currency = currency
                coin.save()
        return

    def test_result(self, ret, result_type=list):
        self.assertEqual(ret['success'], True)
        self.assertEqual(ret['message'], "")
        if type(result_type) is list:
            self.assertIn(type(ret['result']), result_type)
        else:
            self.assertIs(type(ret['result']), result_type)

    def getPrice(self, currency_symbol):
        try:
            pair = 'X' + currency_symbol + 'Z' + self.comparison_currency
            res = self.kraken.query_public('OHLC', data= {'pair': pair, 'since' : self.since, 'interval': 21600 })
            return res['result'][pair]
        except:
           return 0