from django.apps import AppConfig


class DatabaseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "manaql.database"
    label = "database"
