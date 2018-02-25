import logging
from django.core.exceptions import ObjectDoesNotExist
from DimeCoins.models.coins0 import *
from DimeCoins.models.coins70 import *
from DimeCoins.models.coins140 import *
from DimeCoins.models.coins210 import *
from DimeCoins.models.coins280 import *
from DimeCoins.models.coins350 import *
from DimeCoins.models.coins490 import *
from DimeCoins.models.coins560 import *
from DimeCoins.models.coins630 import *
from DimeCoins.models.coins700 import *
from DimeCoins.models.coins770 import *
from DimeCoins.models.coins840 import *
from DimeCoins.models.coins910 import *
from DimeCoins.models.coins980 import *
from DimeCoins.models.coins1050 import *
from DimeCoins.models.coins1120 import *
from DimeCoins.models.coins1190 import *
from DimeCoins.models.coins1260 import *
from DimeCoins.models.coins1330 import *
from DimeCoins.models.coins1470 import *
from DimeCoins.models.coins1540 import *
from DimeCoins.models.coins1610 import *
from DimeCoins.models.coins1680 import *
from DimeCoins.models.coins1750 import *
from DimeCoins.models.coins1890 import *
from DimeCoins.models.coins1960 import *
from DimeCoins.models.coins2030 import *
from DimeCoins.models.coins2100 import *
from DimeCoins.models.coins2170 import *

logger = logging.getLogger(__name__)


class Coins:

    def __init__(self):
        pass

    def get_coin_type(self,  symbol, time, exchange):
        symbol = self.parse_symbol(symbol)
        try:
            coin_class = eval(symbol)
            return coin_class.objects.get(time=time, xchange=exchange)
        except ObjectDoesNotExist:
            return eval(symbol)()

    @staticmethod
    def parse_symbol(symbol):
        new_symbol = ""
        for idx, char in enumerate(symbol):
            if idx == 0:
                if char.isdigit():
                    if int(char) == 1:
                        new_symbol = new_symbol + 'ONE_'
                    if int(char) == 2:
                        new_symbol = new_symbol + 'TWO_'
                    if int(char) == 3:
                        new_symbol = new_symbol + 'THREE_'
                    if int(char) == 4:
                        new_symbol = new_symbol + 'FOUR_'
                    if int(char) == 5:
                        new_symbol = new_symbol + 'FIVE_'
                    if int(char) == 6:
                        new_symbol = new_symbol + 'SIX_'
                    if int(char) == 7:
                        new_symbol = new_symbol + 'SEVEN_'
                    if int(char) == 8:
                        new_symbol = new_symbol + 'EIGHT_'
                    if int(char) == 9:
                        new_symbol = new_symbol + 'NINE_'
                    if int(char) == 0:
                        new_symbol = new_symbol + 'ZERO_'
                elif char.encode('ascii').isalpha():
                    new_symbol = new_symbol + char
                else:
                    pass
            else:
                if char.encode('ascii').isalpha() or char.isdigit():
                    new_symbol = new_symbol + char

        return new_symbol
