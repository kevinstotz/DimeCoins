from DimeCoins.models import Currency
from DimeCoins.classes.Xchanges import CryptoCompare2, Gdax, CoinMarketCap, Coinbase, CoinApi, CoinDesk, Bittrex, Kraken
import logging
from rest_framework.renderers import JSONRenderer
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

logger = logging.getLogger(__name__)


class Index(generics.GenericAPIView):
    permission_classes = (AllowAny, )
    model = Currency
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)

    def get(self, request, *args, **kwargs):

        exchange = CoinMarketCap.CoinMarketCap()
        exchange.get()

        exchange = CoinDesk.CoinDesk()
        exchange.get()

        exchange = CoinDesk.CoinDesk()
        exchange.get()

        exchange = Bittrex.Bittrex()
        exchange.get()

        exchange = Kraken.Kraken()
        exchange.get()

        exchange = CoinApi.CoinApi()
        exchange.get()

        exchange = Coinbase.Coinbase()
        exchange.get()

        exchange = Gdax.Gdax()
        exchange.get()

        exchange = CryptoCompare2.CryptoCompare()
        exchange.get()

        return Response(status=status.HTTP_200_OK)