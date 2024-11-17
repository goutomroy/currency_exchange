from rest_framework.exceptions import NotFound

from apps.exchange.models.currency import Currency


class CurrencyValidationMixin:
    def get_currency(self, code: str, currency_type: str):
        try:
            return Currency.objects.get(code=code)
        except Currency.DoesNotExist:
            raise NotFound(f"{currency_type} '{code}' not found.")
