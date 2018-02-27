import logging
import inspect
from DimeCoins.classes.SymbolName import SymbolName
from django.core.exceptions import ObjectDoesNotExist
from DimeCoins.models.coins0 import *
from DimeCoins.models.coins70 import *
from DimeCoins.models.coins140 import *
from DimeCoins.models.coins210 import *
from DimeCoins.models.coins280 import *
from DimeCoins.models.coins350 import *
from DimeCoins.models.coins420 import *
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
from DimeCoins.models.coins1400 import *
from DimeCoins.models.coins1470 import *
from DimeCoins.models.coins1540 import *
from DimeCoins.models.coins1610 import *
from DimeCoins.models.coins1680 import *
from DimeCoins.models.coins1750 import *
from DimeCoins.models.coins1820 import *
from DimeCoins.models.coins1890 import *
from DimeCoins.models.coins1960 import *
from DimeCoins.models.coins2030 import *
from DimeCoins.models.coins2100 import *
from DimeCoins.models.coins2170 import *
from DimeCoins.models.coins2240 import *
from DimeCoins.models.coins2310 import *
from DimeCoins.models.coins2380 import *
from DimeCoins.models.coins2450 import *
from DimeCoins.models.coins2520 import *


logger = logging.getLogger(__name__)


class Coins:

    def __init__(self):
        pass

    def get_coin_type(self,  symbol, time, exchange):
        symboName = SymbolName(symbol)
        symbol = symboName.parse_symbol()

        if inspect.getmembers(symbol):
            try:
                coin_class = eval(symbol)
                return coin_class.objects.get(time=time, xchange=exchange)
            except ObjectDoesNotExist:
                return eval(symbol)()
            except NameError:
                return None
        else:
            return None