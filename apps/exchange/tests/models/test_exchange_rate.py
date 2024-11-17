from model_bakery import baker
from rest_framework.test import APITestCase

from apps.exchange.models.currency import Currency
from apps.exchange.models.exchange_rate import ExchangeRate


class ExchangeRateModelTests(APITestCase):
    def test_exchange_rate_creation(self):
        """Test exchange rate created"""
        base_currency = baker.make(Currency, code="GBP")
        target_currency = baker.make(Currency, code="EUR")
        baker.make(
            ExchangeRate,
            base_currency=base_currency,
            target_currency=target_currency,
        )
        self.assertEqual(ExchangeRate.objects.count(), 1)
