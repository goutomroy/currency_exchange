from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics
from rest_framework.exceptions import NotFound

from apps.exchange.models.currency import Currency
from apps.exchange.models.exchange_rate import ExchangeRate
from apps.exchange.serializers.exchange_rate import ExchangeRateSerializer


class ExchangeRateDetailView(generics.RetrieveAPIView):
    serializer_class = ExchangeRateSerializer

    def get_queryset(self):
        base_currency = self._validate_currency(
            self.kwargs["base_currency_code"], "Base currency"
        )
        target_currency = self._validate_currency(
            self.kwargs["target_currency_code"], "Target currency"
        )

        return (
            ExchangeRate.objects.select_related("base_currency", "target_currency")
            .filter(base_currency=base_currency, target_currency=target_currency)
            .order_by("-created")
        )

    def get_object(self):
        exchange_rate = self.get_queryset().first()

        if not exchange_rate:
            raise NotFound("Exchange rate not found.")

        return exchange_rate

    @method_decorator(
        cache_page(None, key_prefix=settings.CACHE_KEY_PREFIX_EXCHANGE_RATE)
    )  # cache response for forever
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def _validate_currency(self, code: str, currency_type: str):
        try:
            return Currency.objects.get(code=code)
        except Currency.DoesNotExist:
            raise NotFound(f"{currency_type} '{code}' not found.")
