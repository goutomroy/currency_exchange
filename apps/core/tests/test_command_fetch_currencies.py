from unittest.mock import MagicMock, patch

import requests
from django.core.management import call_command
from django.test import TestCase
from model_bakery import baker

from apps.exchange.models.currency import Currency


class FetchCurrenciesCommandTests(TestCase):
    @patch("apps.core.management.commands.fetch_currencies.requests.get")
    @patch("apps.core.management.commands.fetch_currencies.logger")
    def test_successful_fetch_and_save(self, mock_logger, mock_get):
        """Test that currencies are successfully fetched and saved to the database."""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "response": [
                {
                    "id": 1,
                    "name": "UAE Dirham",
                    "short_code": "AED",
                    "code": "784",
                    "precision": 2,
                    "subunit": 100,
                    "symbol": "د.إ",
                    "symbol_first": True,
                    "decimal_mark": ".",
                    "thousands_separator": ",",
                }
            ],
        }
        mock_get.return_value = mock_response

        call_command("fetch_currencies")

        # Assert that currency data is saved to the database
        self.assertTrue(Currency.objects.filter(code="AED").exists())
        currency = Currency.objects.get(code="AED")
        self.assertEqual(currency.name, "UAE Dirham")
        self.assertEqual(currency.numeric_code, "784")

        # Assert logging calls
        mock_logger.info.assert_any_call("Successfully fetched currency data.")
        mock_logger.info.assert_any_call(
            "Currencies uploaded successfully to the database."
        )

    @patch("apps.core.management.commands.fetch_currencies.requests.get")
    @patch("apps.core.management.commands.fetch_currencies.logger")
    def test_api_error_handling(self, mock_logger, mock_get):
        """Test that the command logs an error when the API response code is not 200."""
        # Mock API response with error code
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"meta": {"code": 400}}
        mock_get.return_value = mock_response

        call_command("fetch_currencies")

        # Assert error log and no data saved
        mock_logger.error.assert_called_with(
            "Failed to fetch currencies: Invalid response code."
        )
        self.assertEqual(Currency.objects.count(), 0)

    @patch("apps.core.management.commands.fetch_currencies.requests.get")
    @patch("apps.core.management.commands.fetch_currencies.logger")
    def test_empty_response_handling(self, mock_logger, mock_get):
        """Test that the command handles an empty 'response' key gracefully."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"meta": {"code": 200}, "response": []}
        mock_get.return_value = mock_response

        call_command("fetch_currencies")

        # Assert error log and no data saved
        mock_logger.error.assert_called_with("Empty response: No item in response")
        self.assertEqual(Currency.objects.count(), 0)

    @patch("apps.core.management.commands.fetch_currencies.requests.get")
    @patch("apps.core.management.commands.fetch_currencies.logger")
    def test_request_exception_handling(self, mock_logger, mock_get):
        """Test that the command logs an error when a network exception occurs."""
        # Simulate a network exception
        mock_get.side_effect = requests.RequestException("Network error")

        call_command("fetch_currencies")

        # Assert error log and no data saved
        mock_logger.error.assert_called_with(
            "Failed to fetch currencies from API: Network error"
        )
        self.assertEqual(Currency.objects.count(), 0)

    @patch("apps.core.management.commands.fetch_currencies.requests.get")
    @patch("apps.core.management.commands.fetch_currencies.logger")
    def test_currency_update_existing(self, mock_logger, mock_get):
        """Test that existing currency data is updated if it already exists."""
        # Create initial currency object with different data
        currency = baker.make(
            Currency,
            code="AED",
            name="Old Name",
            numeric_code="123",
            precision=1,
            subunit=50,
            symbol="X",
            symbol_first=False,
            decimal_mark=",",
            thousands_separator=".",
        )

        # Mock API response with updated data for the same currency
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meta": {"code": 200},
            "response": [
                {
                    "id": 1,
                    "name": "UAE Dirham",
                    "short_code": "AED",
                    "code": "784",
                    "precision": 2,
                    "subunit": 100,
                    "symbol": "د.إ",
                    "symbol_first": True,
                    "decimal_mark": ".",
                    "thousands_separator": ",",
                }
            ],
        }
        mock_get.return_value = mock_response

        call_command("fetch_currencies")

        # Verify that the currency data was updated
        currency.refresh_from_db()
        self.assertEqual(currency.name, "UAE Dirham")
        self.assertEqual(currency.numeric_code, "784")
        self.assertEqual(currency.precision, 2)
        self.assertEqual(currency.subunit, 100)
        self.assertEqual(currency.symbol, "د.إ")
        self.assertTrue(currency.symbol_first)
        self.assertEqual(currency.decimal_mark, ".")
        self.assertEqual(currency.thousands_separator, ",")
