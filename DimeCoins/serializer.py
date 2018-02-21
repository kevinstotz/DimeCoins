from datetime import datetime
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from models import BitCoin


class DimeIndexSerializer(ModelSerializer):

    class Meta:
        model = BitCoin
        fields = ('id', 'currency',)

