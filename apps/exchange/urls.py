from django.urls import path

from apps.exchange.views.currency import CurrencyListView
from apps.exchange.views.exchange_rate import ExchangeRateDetailView

urlpatterns = [
    path("currency/", CurrencyListView.as_view(), name="currency-list"),
    path(
        "currency/<str:base_currency_code>/<str:target_currency_code>/",
        ExchangeRateDetailView.as_view(),
        name="exchange-rate-detail",
    ),
]
