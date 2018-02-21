from DimeCoins.models import Xchange, Currency
from DimeCoins.settings.base import XCHANGE
from DimeCoins.classes import Coins
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, time
import logging
import time
import requests

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',
                    )


class CryptoCompare:

    def __init__(self, xchange=XCHANGE['CRYPTO_COMPARE'], comparison_currency='USD'):
        #  instance variable unique to each instance

        self.xchange = Xchange.objects.get(pk=xchange)
        self.comparison_currency = comparison_currency
        self.coin_list_url = 'https://www.cryptocompare.com/api/data/coinlist/'
        self.history = '/histoday?fsym=BTC&tsym=USD&limit=60&aggregate=1&toTs=1452680400'

    def get(self):

        currencies = Currency.objects.all()

        for currency in currencies:
            res = self.getPrice(currency.symbol, int(time.time()), 10)

            coins = Coins.Coins()
            if res == 0 or res == [] or res == None or type(res) == 'NoneType':
                continue
            print(res)

            for price in res:
                print(price)
                coin = coins.get_coin_type(symbol=currency.symbol, time=price['time'], exchange=self.xchange)
                coin.time = price['time']
                coin.open = float(price['open'])
                coin.close = float(price['close'])
                coin.high = float(price['high'])
                coin.low = float(price['low'])
                coin.xchange = self.xchange
                coin.currency = currency
                coin.save()
        return 0

    def getPrice(self, currency_symbol, start_date=datetime.utcnow().timetuple(), count=2):
        url = '{0}/histoday?fsym={1}&tsym={2}&aggregate=1&Tots={3}&limit={4}'.format(self.xchange.api_url,
                                                                                     currency_symbol,
                                                                                     self.comparison_currency,
                                                                                     start_date,
                                                                                     count)
        spot_price = requests.get(url).json()
        if spot_price['Response'] == 'Success':
            return spot_price['Data']
        else:
            return 0

    def getCoinSnapShot(self, currency_symbol):
        url = '{0}/coinsnapshot?fsym={1}&tsym={2}'.format(self.xchange.api_url,
                                                          currency_symbol,
                                                          self.comparison_currency)
        snap_shot_reponse = requests.get(url)
        return snap_shot_reponse.json()

    def getCoinMarketCap(self, currency_symbol):
        coin_snap_shot = self.getCoinSnapShot(currency_symbol)
        return coin_snap_shot.Data.TotalCoinsMined
