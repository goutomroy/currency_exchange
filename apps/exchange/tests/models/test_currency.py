from model_bakery import baker
from rest_framework.test import APITestCase

from apps.exchange.models.currency import Currency


class CurrencyModelTests(APITestCase):
    def test_currency_creation(self):
        """Test currency created"""
        baker.make(Currency, code="USD")
        self.assertEqual(Currency.objects.count(), 1)
