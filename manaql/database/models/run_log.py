from enum import Enum

from django.db import models
from django.utils.timezone import now


class Command(str, Enum):
    Download = "download"
    Ingest = "ingest"
    Process = "process"
    All = "all"

    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]


class RunLog(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.CharField(max_length=255, null=False, unique=False)
    command = models.CharField(max_length=31, null=False, choices=Command.choices())
    created_at = models.DateTimeField(default=now)

    class Meta:
        db_table = "run_log"
