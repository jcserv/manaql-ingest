import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ingest.settings")
import django

django.setup()
