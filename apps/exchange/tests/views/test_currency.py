from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from apps.exchange.models.currency import Currency


class CurrencyListViewTests(APITestCase):
    def setUp(self):
        # Create multiple Currency instances
        self.currencies = baker.make(Currency, _quantity=5)

    def test_currency_list_view(self):
        """Test retrieving a list of currencies"""
        url = reverse("currency-list")
        response = self.client.get(url)

        # Verify response status
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify response content
        self.assertEqual(len(response.data), len(self.currencies))
        for item in response.data:
            self.assertIn("code", item)
