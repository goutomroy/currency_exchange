from django.db import models

from apps.core.models import BaseModel
from apps.exchange.models.currency import Currency


class ExchangeRate(BaseModel):
    base_currency = models.ForeignKey(
        Currency, related_name="base_currency", on_delete=models.CASCADE
    )
    target_currency = models.ForeignKey(
        Currency, related_name="target_currency", on_delete=models.CASCADE
    )
    rate = models.DecimalField(max_digits=18, decimal_places=8)

    class Meta:
        unique_together = ("base_currency", "target_currency", "created")

    def __str__(self):
        return f"{self.currency_pair_display} - {self.rate}"

    @property
    def currency_pair_display(self):
        return f"{self.base_currency.code}{self.target_currency.code}"
