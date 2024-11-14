from django.contrib import admin

from apps.exchange.models.currency import Currency
from apps.exchange.models.exchange_rate import ExchangeRate


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("code",)
    ordering = ("code",)


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ("base_currency", "target_currency", "rate", "created")
    list_filter = ("base_currency", "target_currency", "created")
    ordering = ("base_currency", "target_currency", "rate")
