from DimeCoins.models.base import Xchange, Currency
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from DimeCoins.classes import Coins, SymbolName
from DimeCoins.settings.base import XCHANGE
from datetime import datetime, timedelta
import datetime
import logging
import requests
import calendar
from bs4 import BeautifulSoup


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',
                    )


class Command(BaseCommand):
    xchange = Xchange.objects.get(pk=XCHANGE['COIN_MARKET_CAP'])
    comparison_currency = 'USD'

    def handle(self, *args, **options):
        #  instance variable unique to each instance

        now = datetime.datetime.now()
        end_date = start_date = now.replace(second=0, minute=0, hour=0)
        start_date = start_date - timedelta(days=7)
        currencies = Currency.objects.all()
        currencies= [
            [0, 'BTC', 'bitcoin'],
            [1, 'BTS', 'bitshares'],
            [2, 'ETH', 'Ethereum'],
            [3, 'LTC', 'Litecoin'],
            [4, 'XRP', 'Ripple'],
            [5, 'XMR', 'Monero'],
            [6, 'ETC', 'Ethereum-Classic'],
            [7, 'DSH', 'DASHcoin'],
            [8, 'MAID', 'MaidSafeCoin'],
            [9, 'XEM', 'NEM'],
            [10, 'STEEM', 'STEEM'],
            [11, 'REP', 'Augur'],
            [12, 'ICN', 'Iconomi'],
            [13, 'ZEC', 'ZCash'],
            [14, 'WAVES', 'Waves'],
            [15, 'LSK', 'Lisk'],
            [16, 'DOGE', 'Dogecoin'],
            [17, 'MIOTA', 'IOTA'],
            [18, 'NEO', 'NEO'],
            [19, 'OMG', 'omisego'],
            [20, 'BTG', 'Bitcoin-Gold'],
            [21, 'EOS', 'EOS'],
            [22, 'ADA', 'Cardano'],
            [23, 'BCH', 'Bitcoin-Cash'],
            [24, 'DASH', 'dash'],
            [25, 'XLM', 'stellar']
        ]
        for currency in currencies:
            self.parseHistoricalPage(currency, start_date, end_date)
        quit()

        now = datetime.datetime.now()
        start_date = now.replace(second=0, minute=0, hour=0)
        start_date = start_date - timedelta(days=1)
        end_date = start_date - timedelta(weeks=1)

        while end_date < start_date:
            self.parse(start_date)
            start_date = start_date - timedelta(weeks=1)

    def parseHistoricalPage(self, currency_c, start_date, end_date):

        r = requests.get('https://coinmarketcap.com/currencies/{0}/historical-data/?start={1}&end={2}'.format(currency_c[2].lower(),
                                                                                                              start_date.strftime('%Y%m%d'),
                                                                                                              end_date.strftime('%Y%m%d')))
        if r.status_code != 200:
            print("not found {0}".format(r.url))
            return

        soup = BeautifulSoup(r.content, "html.parser")

        table = soup.find('tbody')

        for row in table.findAll('tr'):
            cells = row.findAll('td')

            try:
                timestamp = datetime.datetime.strptime(cells[0].text.strip(), "%b %d, %Y").date()
            except:
                timestamp = 0

            try:
                open = float(cells[1].text.strip())
            except:
                open = 0

            try:
                high = float(cells[2].text.strip())
            except:
                high = 0

            try:
                low = float(cells[3].text.strip())
            except:
                low = 0

            try:
                close = float(cells[4].text.strip())
            except:
                close = 0

            try:
                volume = int(cells[5].text.replace(',', ''))
            except:
                volume = 0

            try:

                market_cap = int(cells[6].text.replace(',', ''))
            except:
                market_cap  = 0

            new_symbol = SymbolName.SymbolName(currency_c[1])

            try:
                currency = Currency.objects.get(symbol=new_symbol.parse_symbol())
            except ObjectDoesNotExist as error:
                print(symbol + " does not exist in our currency list..continuing")
                continue
                currency = Currency()
                currency.symbol = new_symbol.parse_symbol()
                try:
                    currency.save()
                    currency = Currency.objects.get(symbol=currency.symbol)
                    print(symbol)
                except:
                    print("failed adding {0}".format(currency.symbol))
                    continue

            coins = Coins.Coins()

            coin = coins.get_coin_type(symbol=new_symbol.symbol, time=int(calendar.timegm(timestamp.timetuple())), exchange=self.xchange)
            if coin is not None:
                coin.xchange = self.xchange
                coin.open = open
                coin.close = close
                coin.high = high
                coin.low = low
                coin.volume = volume
                coin.currency = currency
                coin.time = int(calendar.timegm(timestamp.timetuple()))
                coin.market_cap = market_cap
                coin.save()
            else:
                print("no class " + symbol)
        return


    def parse(self, start_date):

        r = requests.get('https://coinmarketcap.com/historical/{0}/'.format(start_date.strftime('%Y%m%d')))
        if r.status_code != 200:
            print("not found {0}".format(r.url))
            return
        soup = BeautifulSoup(r.content, "html.parser")

        table = soup.find('tbody')

        for row in table.findAll('tr'):
            cells = row.findAll('td')
            symbol = cells[1].span.a.text
            symbol = cells[2].text.strip()

            market_cap = cells[3]['data-usd']
            try:
                market_cap = float(market_cap)
            except:
                market_cap = 0

            try:
                price = float(cells[4].a['data-usd'])
            except:
                price = 0

            try:
                circulating_supply = cells[5].a['data-supply']
            except:
                circulating_supply = cells[5].span['data-supply']

            try:
                circulating_supply = int(float(circulating_supply))
            except:
                circulating_supply  = 0

            new_symbol = SymbolName.SymbolName(symbol)

            try:
                currency = Currency.objects.get(symbol=new_symbol.parse_symbol())
            except ObjectDoesNotExist as error:
                print(symbol + " does not exist in our currency list..continuing")
                continue
                currency = Currency()
                currency.symbol = new_symbol.parse_symbol()
                try:
                    currency.save()
                    currency = Currency.objects.get(symbol=currency.symbol)
                    print(symbol)
                except:
                    print("failed adding {0}".format(currency.symbol))
                    continue

            coins = Coins.Coins()

            coin = coins.get_coin_type(symbol=symbol, time=int(calendar.timegm(start_date.timetuple())), exchange=self.xchange)
            if coin is not None:
                coin.xchange = self.xchange
                coin.close = price
                coin.currency = currency
                coin.time = int(calendar.timegm(start_date.timetuple()))
                coin.market_cap = market_cap
                coin.total_supply = circulating_supply
                coin.save()
            else:
                print("no class " + symbol)
        return

    def __date_to_iso8601(self, date_time):
        return '{year}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}'.format(
            year=date_time.tm_year,
            month=date_time.tm_mon,
            day=date_time.tm_mday,
            hour=date_time.tm_hour,
            minute=date_time.tm_min,
            second=date_time.tm_sec)
