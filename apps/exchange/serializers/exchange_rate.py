from rest_framework import serializers

from apps.exchange.models.exchange_rate import ExchangeRate


class ExchangeRateSerializer(serializers.ModelSerializer):
    currency_pair = serializers.CharField(
        source="currency_pair_display", read_only=True
    )

    class Meta:
        model = ExchangeRate
        fields = ["currency_pair", "rate"]
