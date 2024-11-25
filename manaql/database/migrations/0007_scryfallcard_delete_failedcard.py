# Generated by Django 5.1.3 on 2024-11-25 20:56

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("database", "0006_failedcard"),
    ]

    operations = [
        migrations.CreateModel(
            name="ScryfallCard",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, null=True)),
                ("lang", models.CharField(max_length=5, null=True)),
                ("set_code", models.CharField(max_length=7, null=True)),
                ("set_name", models.CharField(max_length=255, null=True)),
                ("collector_number", models.CharField(max_length=7, null=True)),
                ("type_line", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "finishes",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=20),
                        default=list,
                        size=None,
                    ),
                ),
                ("prices", models.JSONField(default=dict, null=True)),
                ("image_uris", models.JSONField(null=True)),
                ("card_faces", models.JSONField(null=True)),
            ],
            options={
                "db_table": "scryfall_card",
            },
        ),
        migrations.DeleteModel(
            name="FailedCard",
        ),
    ]
