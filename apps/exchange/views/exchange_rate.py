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
        base_currency_code = self.kwargs["base_currency_code"]
        target_currency_code = self.kwargs["target_currency_code"]

        try:
            base_currency = Currency.objects.get(code=base_currency_code)
        except Currency.DoesNotExist:
            raise NotFound(f"Base Currency '{base_currency_code}' not found.")  # noqa

        try:
            target_currency = Currency.objects.get(code=target_currency_code)
        except Currency.DoesNotExist:
            raise NotFound(
                f"Target Currency '{target_currency_code}' not found."  # noqa
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
