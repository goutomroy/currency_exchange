from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import filters, generics

from apps.exchange.models.currency import Currency
from apps.exchange.serializers.currency import CurrencySerializer
from apps.exchange.throttles import AnonymousRateThrottle


class CurrencyListView(generics.ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    throttle_classes = [AnonymousRateThrottle]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = [
        "code",
    ]

    def get_queryset(self):
        return super().get_queryset().order_by("code")

    @method_decorator(cache_page(60 * 60 * 24))  # cache response for 24 hours
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
