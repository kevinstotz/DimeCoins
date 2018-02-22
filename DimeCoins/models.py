from __future__ import unicode_literals
from django.db import models
from .settings.base import CURRENCY_NAME_LENGTH, COIN_SYMBOL_LENGTH


class Xchange(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default="")
    url = models.CharField(max_length=200, default="")
    api_url = models.CharField(max_length=200, default="")
    api_key =  models.CharField(max_length=200, default="")
    api_secret =  models.CharField(max_length=200, default="")

    objects = models.Manager()

    def __str__(self):
        return '%s' % self.name

    class Meta:
        ordering = ('name',)


class Currency(models.Model):
    id = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=COIN_SYMBOL_LENGTH, default="")

    objects = models.Manager()


class Coin(models.Model):
    id = models.AutoField(primary_key=True)
    xchange = models.ForeignKey(Xchange, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    time = models.BigIntegerField(verbose_name="Date of Price", default=0)
    open = models.FloatField(default=0.0)
    close = models.FloatField(default=0.0)
    high = models.FloatField(default=0.0)
    low = models.FloatField(default=0.0)
    total_supply = models.FloatField(default=0.0)
    volume = models.FloatField(default=0.0)
    market_cap = models.FloatField(default=0.0)

    objects = models.Manager()

    class Meta:
        abstract = True


class ADA(Coin):
    pass


class BCH(Coin):
    pass


class BTC(Coin):
    pass


class BTG(Coin):
    pass


class CRIX(Coin):
    pass


class DASH(Coin):
    pass


class DOGE(Coin):
    pass


class DSH(Coin):
    pass


class EOS(Coin):
    pass


class ETC(Coin):
    pass


class ETH(Coin):
    pass


class ICN(Coin):
    pass


class IOTA(Coin):
    pass


class LSK(Coin):
    pass


class LTC(Coin):
    pass


class MAID(Coin):
    pass


class MIOTA(Coin):
    pass


class NEO(Coin):
    pass


class OMGC(Coin):
    pass


class REP(Coin):
    pass


class STEEM(Coin):
    pass


class WAVES(Coin):
    pass


class XEM(Coin):
    pass


class XLM(Coin):
    pass


class XMR(Coin):
    pass


class XRP(Coin):
    pass


class ZEC(Coin):
    pass
