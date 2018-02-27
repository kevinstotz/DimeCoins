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
        start_date = now.replace(year=2018, month=2, day=25, second=0, minute=0, hour=0)
        start_date = start_date - timedelta(weeks=0)
        end_date = start_date - timedelta(weeks=3)

        while end_date < start_date:
            self.parse(start_date)
            start_date = start_date - timedelta(weeks=1)

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
