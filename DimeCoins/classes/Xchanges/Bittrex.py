from DimeCoins.models import Xchange, Currency
from DimeCoins.classes import Coins
from bittrex_v2 import Bittrex as Bittrex_mod, BittrexError
from django.core.exceptions import ObjectDoesNotExist
from DimeCoins.settings.base import XCHANGE
from datetime import datetime
import logging
from decimal import Decimal

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',
                    )


class Bittrex:

    def __init__(self, xchange=XCHANGE['BITTREX'], comparison_currency='USD'):
        #  instance variable unique to each instance
        self.valid_periods = ("oneMin", "fiveMin", "thirtyMin", "hour", "day")
        self.SHOW_ENDPOINTS = False
        self.TIMEOUT = 30

        self.xchange = Xchange.objects.get(pk=xchange)
        try:
            self.bittrex = Bittrex_mod(api_key=self.xchange.api_key,
                                   api_secret=self.xchange.api_secret,
                                   timeout=self.TIMEOUT,
                                   debug_endpoint=self.SHOW_ENDPOINTS,
                                   parse_float=Decimal)
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
                utc_dt = datetime.strptime(price['T'], '%Y-%m-%dT%H:%M:%S')
                timestamp = (utc_dt - datetime(1970, 1, 1)).total_seconds()
                coin = coins.get_coin_type(symbol=currency.symbol, time=int(timestamp), exchange=self.xchange)
                coin.time = int(timestamp)
                coin.open = float(price['O'])
                coin.close = float(price['C'])
                coin.high = float(price['H'])
                coin.low = float(price['L'])
                coin.volume = float(price['V'])
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
            res = self.bittrex.get_ticks(market='USDT-' + currency_symbol, period='day')
            return res['result']
        except:
           return 0