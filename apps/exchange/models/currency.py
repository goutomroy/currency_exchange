from django.db import models

from apps.core.models import BaseModel


class Currency(BaseModel):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)
    numeric_code = models.CharField(max_length=3)
    precision = models.IntegerField()
    subunit = models.IntegerField()
    symbol = models.CharField(max_length=5)
    symbol_first = models.BooleanField()
    decimal_mark = models.CharField(max_length=1)
    thousands_separator = models.CharField(max_length=1)

    def __str__(self):
        return f"{self.name} ({self.code})"
