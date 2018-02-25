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

    def handle(self, *args, **options):
        #  instance variable unique to each instance

        self.xchange = Xchange.objects.get(pk=XCHANGE['COIN_MARKET_CAP'])
        self.comparison_currency = 'USD'
        self.coin_list_url = ''

        now = datetime.now()
        start_date = now.replace(second=0, minute=0, hour=0)
        end_date = start_date - timedelta(days=10)
        id = 0

        while end_date < start_date:
            start_date = start_date - timedelta(days=1)
            self.parse(start_date)

    def getPrice(self, currency_symbol, start_date, end_date, granularity=86400):
        params = {'granularity': granularity,
                   'start': start_date,
                   'end': end_date}

        headers = {'content-type': 'application/json','user-agent': 'your-own-user-agent/0.0.1'}
        spot_price = requests.get(self.xchange.api_url + '/products/' + currency_symbol + '-' +
                                  self.comparison_currency + '/candles?granularity={0}&start={1}&end={2}'.format(granularity, start_date, end_date), headers=headers)
        if spot_price.status_code == requests.codes.ok:
            return spot_price.json()
        else:
            return([])

    def getCoins(self):
        headers = {'content-type': 'application/json',
                   'user-agent': 'your-own-user-agent/0.0.1'}
        params = {}
        currencies = requests.get(self.coin_list_url, params=params, headers=headers)
        return currencies.json()['Data']

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
                print(symbol + " exists")
            except ObjectDoesNotExist as error:
                print(symbol + " does not exist in our currency list..adding")
                currency = Currency()
                currency.symbol = new_symbol.parse_symbol()
                try:
                    currency.save()
                    currency = Currency.objects.get(symbol=currency.symbol)
                    print("added")
                except:
                    print("failed adding {0}".format(currency.symbol))
                    continue

            coins = Coins.Coins()

            coin = coins.get_coin_type(symbol=currency.symbol, time=int(calendar.timegm(start_date.timetuple())), exchange=self.xchange)
            coin.xchange = self.xchange
            coin.close = price
            coin.currency = currency
            coin.time = int(calendar.timegm(start_date.timetuple()))
            coin.market_cap = market_cap
            coin.total_supply = circulating_supply
            coin.save()
        return



    def __date_to_iso8601(self, date_time):
        return '{year}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}'.format(
            year=date_time.tm_year,
            month=date_time.tm_mon,
            day=date_time.tm_mday,
            hour=date_time.tm_hour,
            minute=date_time.tm_min,
            second=date_time.tm_sec)
