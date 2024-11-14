import logging
import os
from decimal import ROUND_DOWN, Decimal

import requests
from celery import shared_task
from django.db import IntegrityError
from django.utils import timezone

from apps.exchange.models.currency import Currency
from apps.exchange.models.exchange_rate import ExchangeRate

logger = logging.getLogger("workers")

API_URL = "https://api.currencybeacon.com/v1/historical"
API_KEY = os.environ.get("BEACON_API_KEY", "")


@shared_task
def root_fetcher():
    logger.info("root fetcher executed")

    # It's for development purpose only, originally we need to fetch our currency model
    pairs = sorted(["EUR", "PLN", "USD", "JPY"])

    for index in range(len(pairs) - 1):
        from_currency, to_currencies = pairs[index], pairs[index + 1 :]
        fetch_from_currency.delay(from_currency, ",".join(to_currencies))


@shared_task
def fetch_from_currency(from_currency: str, symbols: str):
    logger.info(f"{from_currency}  {symbols}")
    date = timezone.now().strftime("%Y-%m-%d")
    params = {
        "base": from_currency,
        "symbols": symbols,
        "date": date,
        "api_key": API_KEY,
    }

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"API request failed for {from_currency} to {symbols}: {e}")
        return
    logger.info(response.json())
    data = response.json().get("response", {}).get("rates", {})
    if not data:
        logger.error(
            f"No rates found in API response for {from_currency} to {symbols}: {response.json()}"  # noqa
        )
        return

    base_currency = Currency.objects.filter(code=from_currency).first()
    if not base_currency:
        logger.warning(f"Base currency not found: {from_currency}")
        return

    for to_currency_code, rate_value in data.items():
        target_currency = Currency.objects.filter(code=to_currency_code).first()
        if not target_currency:
            logger.warning(f"Target currency not found: {to_currency_code}")
            continue

        try:
            rate_value = Decimal(rate_value).quantize(
                Decimal("0.0001"), rounding=ROUND_DOWN
            )
            ExchangeRate.objects.create(
                base_currency=base_currency,
                target_currency=target_currency,
                created=timezone.now(),
                rate=rate_value,
            )

            logger.info(
                f"Exchange rate saved: {from_currency} to {to_currency_code} = {rate_value}"  # noqa
            )
        except IntegrityError as e:
            logger.error(
                f"Database error saving rate {from_currency} to {to_currency_code}: {e}"
            )
