from rest_framework import serializers

from apps.exchange.models.currency import Currency


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ["code"]
