from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from apps.exchange.models.currency import Currency
from apps.exchange.models.exchange_rate import ExchangeRate


class ExchangeRateDetailViewTests(APITestCase):
    def setUp(self):
        # Create Currency instances
        self.base_currency = baker.make(Currency, code="EUR")
        self.target_currency = baker.make(Currency, code="USD")
        self.another_currency = baker.make(Currency, code="JPY")

        # Additional exchange rate to ensure ordering by date
        self.old_exchange_rate = baker.make(
            ExchangeRate,
            base_currency=self.base_currency,
            target_currency=self.target_currency,
            rate=1.1,
        )

        # Create ExchangeRate instances
        self.exchange_rate = baker.make(
            ExchangeRate,
            base_currency=self.base_currency,
            target_currency=self.target_currency,
            rate=1.2,
        )

    def test_exchange_rate_detail_view_existing_pair(self):
        """Test retrieving the latest exchange rate for an existing currency pair"""
        url = reverse(
            "exchange-rate-detail",
            args=[self.base_currency.code, self.target_currency.code],
        )
        response = self.client.get(url)

        # Verify response status
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the latest exchange rate is returned
        self.assertEqual(
            response.data["currency_pair"],
            f"{self.base_currency.code}{self.target_currency.code}",
        )
        self.assertEqual(float(response.data["rate"]), self.exchange_rate.rate)

    def test_exchange_rate_detail_view_no_exchange_rate(self):
        """Test the response when no exchange rate exists for a currency pair"""
        url = reverse(
            "exchange-rate-detail",
            args=[self.base_currency.code, self.another_currency.code],
        )
        response = self.client.get(url)

        # Verify response status and error message
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "Exchange rate not found.")

    def test_exchange_rate_detail_view_nonexistent_currency(self):
        """Test the response when a currency code does not exist"""
        url = reverse("exchange-rate-detail", args=["ABC", self.target_currency.code])
        response = self.client.get(url)

        # Verify response status and error message
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Base currency 'ABC' not found.", response.data["detail"])
