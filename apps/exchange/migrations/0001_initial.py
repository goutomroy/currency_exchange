# Generated by Django 5.1.3 on 2024-11-13 23:43

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Currency",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("code", models.CharField(max_length=3, unique=True)),
                ("name", models.CharField(max_length=50)),
                ("numeric_code", models.CharField(max_length=3)),
                ("precision", models.IntegerField()),
                ("subunit", models.IntegerField()),
                ("symbol", models.CharField(max_length=5)),
                ("symbol_first", models.BooleanField()),
                ("decimal_mark", models.CharField(max_length=1)),
                ("thousands_separator", models.CharField(max_length=1)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ExchangeRate",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("rate", models.DecimalField(decimal_places=8, max_digits=18)),
                (
                    "base_currency",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="base_currency",
                        to="exchange.currency",
                    ),
                ),
                (
                    "target_currency",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="target_currency",
                        to="exchange.currency",
                    ),
                ),
            ],
            options={
                "unique_together": {("base_currency", "target_currency", "created")},
            },
        ),
    ]
