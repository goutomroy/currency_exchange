import logging
import os

import requests
from django.conf import settings
from django.core.cache import cache
from django.core.management.base import BaseCommand

from apps.exchange.models.currency import Currency

logger = logging.getLogger("core")


class Command(BaseCommand):
    help = "Fetches and uploads currency data from the Currency Beacon API."

    API_URL = "https://api.currencybeacon.com/v1/currencies"
    API_KEY = os.environ.get("BEACON_API_KEY", "")

    def handle(self, *args, **kwargs):
        """Main entry point for the command."""
        currencies = self._fetch_currencies()
        if currencies:
            self._save_currencies(currencies)
            self._invalidate_cache()

    def _fetch_currencies(self):
        """Fetches currency data from the Currency Beacon API."""
        try:
            response = requests.get(
                self.API_URL, params={"api_key": self.API_KEY, "type": "fiat"}
            )
            response.raise_for_status()  # Raises HTTPError if status code is 4xx or 5xx
            data = response.json()

            if data.get("meta", {}).get("code") != 200:
                logger.error("Failed to fetch currencies: Invalid response code.")
                return None

            currencies = data.get("response")
            if not currencies:
                logger.error("Empty response: No item in response")
                return None

            logger.info("Successfully fetched currency data.")
            return currencies

        except requests.RequestException as e:
            logger.error(f"Failed to fetch currencies from API: {e}")
            return None

    def _save_currencies(self, currencies):
        """Saves the fetched currency data to the database."""
        for currency_data in currencies:
            Currency.objects.update_or_create(
                code=currency_data["short_code"],
                defaults={
                    "name": currency_data["name"],
                    "numeric_code": currency_data["code"],
                    "precision": currency_data["precision"],
                    "subunit": currency_data["subunit"],
                    "symbol": currency_data["symbol"],
                    "symbol_first": currency_data["symbol_first"],
                    "decimal_mark": currency_data["decimal_mark"],
                    "thousands_separator": currency_data["thousands_separator"],
                },
            )

        logger.info("Currencies uploaded successfully to the database.")

    def _invalidate_cache(self):
        cache.delete_pattern(f"*{settings.CACHE_KEY_PREFIX_AVAILABLE_CURRENCIES}:*")
        logger.info(
            f"{settings.CACHE_KEY_PREFIX_AVAILABLE_CURRENCIES} cache invalidated"
        )
