import os
from unittest.mock import MagicMock, call, patch

import requests
from django.test import TestCase
from django.utils import timezone
from model_bakery import baker

from apps.exchange.models.currency import Currency
from apps.exchange.models.exchange_rate import ExchangeRate
from apps.workers.tasks import fetch_from_currency, root_fetcher


class RootFetcherTaskTests(TestCase):
    @patch(
        "apps.workers.tasks.fetch_from_currency.delay"
    )  # Mock the task function itself
    @patch("apps.workers.tasks.logger")
    def test_root_fetcher_task_execution(self, mock_logger, mock_fetch_from_currency):
        """Test that root_fetcher task initiates fetch_from_currency for all currency pairs."""

        # Run root_fetcher
        root_fetcher()

        # Expected calls to fetch_from_currency
        expected_calls = [
            call("EUR", "JPY,PLN,USD"),
            call("JPY", "PLN,USD"),
            call("PLN", "USD"),
        ]

        # Check that fetch_from_currency was called with expected arguments
        self.assertEqual(mock_fetch_from_currency.call_args_list, expected_calls)

        # Assert that root fetcher logs its execution
        mock_logger.info.assert_called_once_with("root fetcher executed")


class FetchFromCurrencyTaskTests(TestCase):
    @patch("apps.workers.tasks.requests.get")
    @patch("apps.workers.tasks.logger")
    def test_successful_fetch_and_save(self, mock_logger, mock_get):
        """Test that exchange rates are fetched and saved successfully."""

        # Setup mock API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "response": {
                "date": "2024-10-15",
                "base": "EUR",
                "rates": {"JPY": 162.4858, "PLN": 4.2933, "USD": 1.0892},
            },
        }
        mock_get.return_value = mock_response

        # Create currency instances
        eur_currency = baker.make(Currency, code="EUR")
        jpy_currency = baker.make(Currency, code="JPY")
        pln_currency = baker.make(Currency, code="PLN")
        usd_currency = baker.make(Currency, code="USD")

        # Run task
        fetch_from_currency("EUR", "JPY,PLN,USD")

        # Assert API request call
        mock_get.assert_called_once_with(
            "https://api.currencybeacon.com/v1/historical",
            params={
                "base": "EUR",
                "symbols": "JPY,PLN,USD",
                "date": timezone.now().strftime("%Y-%m-%d"),
                "api_key": os.environ.get("BEACON_API_KEY", ""),
            },
        )

        # Assert that exchange rates were saved in the database
        self.assertEqual(ExchangeRate.objects.count(), 3)
        self.assertTrue(
            ExchangeRate.objects.filter(
                base_currency=eur_currency,
                target_currency=jpy_currency,
                # rate=Decimal("162.4858"),
            ).exists()
        )
        self.assertTrue(
            ExchangeRate.objects.filter(
                base_currency=eur_currency,
                target_currency=pln_currency,
                # rate=Decimal("4.2933"),
            ).exists()
        )
        self.assertTrue(
            ExchangeRate.objects.filter(
                base_currency=eur_currency,
                target_currency=usd_currency,
                # rate=Decimal("1.0892"),
            ).exists()
        )

        # # Assert logging
        mock_logger.info.assert_any_call("Exchange rate saved: EUR to JPY = 162.4858")
        mock_logger.info.assert_any_call("Exchange rate saved: EUR to PLN = 4.2933")
        # mock_logger.info.assert_any_call("Exchange rate saved: EUR to USD = 1.0892")

    @patch("apps.workers.tasks.requests.get")
    @patch("apps.workers.tasks.logger")
    def test_missing_base_currency(self, mock_logger, mock_get):
        """Test that task logs a warning when the base currency is not found."""
        # No EUR currency in database
        fetch_from_currency("EUR", "USD")

        # Assert warning log for missing base currency
        mock_logger.warning.assert_called_once_with("Base currency not found: EUR")
        self.assertEqual(ExchangeRate.objects.count(), 0)

    @patch("apps.workers.tasks.requests.get")
    @patch("apps.workers.tasks.logger")
    def test_missing_target_currency(self, mock_logger, mock_get):
        """Test that task logs a warning when a target currency is not found."""
        # Create only the base currency EUR
        baker.make(Currency, code="EUR")

        # Mock API response with USD as target currency
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "response": {"rates": {"USD": 1.0892}},
        }
        mock_get.return_value = mock_response

        fetch_from_currency("EUR", "USD")

        # Assert warning log for missing target currency
        mock_logger.warning.assert_called_once_with("Target currency not found: USD")
        self.assertEqual(ExchangeRate.objects.count(), 0)

    @patch("apps.workers.tasks.requests.get")
    @patch("apps.workers.tasks.logger")
    def test_empty_rate_data_handling(self, mock_logger, mock_get):
        """Test that task handles empty 'rates' data in the API response."""
        # Create base currency
        baker.make(Currency, code="EUR")

        # Mock API response with empty rates
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "response": {"rates": {}},
        }
        mock_get.return_value = mock_response

        fetch_from_currency("EUR", "USD")

        # Assert error log for empty rates data
        mock_logger.error.assert_called_once_with(
            "No rates found in API response for EUR to USD: {'meta': {'code': 200}, 'response': {'rates': {}}}"
        )
        self.assertEqual(ExchangeRate.objects.count(), 0)

    @patch("apps.workers.tasks.requests.get")
    @patch("apps.workers.tasks.logger")
    def test_api_request_failure_handling(self, mock_logger, mock_get):
        """Test that task handles API request failures gracefully."""
        # Simulate request exception
        mock_get.side_effect = requests.RequestException("Network error")

        fetch_from_currency("EUR", "USD")

        # Assert error log for request failure
        mock_logger.error.assert_called_once_with(
            "API request failed for EUR to USD: Network error"
        )
        self.assertEqual(ExchangeRate.objects.count(), 0)
