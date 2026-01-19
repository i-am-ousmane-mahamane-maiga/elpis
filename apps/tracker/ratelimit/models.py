# apps/ratelimit/models.py
from django.db import models
from django.conf import settings

from core.models import BaseModel
from core.models import Peer


class RateLimit(BaseModel):
    peer = models.ForeignKey(
        Peer,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    ip = models.GenericIPAddressField()
    endpoint = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "pommezs"
        unique_together = ("peer", "ip", "endpoint", "timestamp")
        indexes = [
            models.Index(fields=["endpoint", "timestamp"]),
            models.Index(fields=["peer"]),
            models.Index(fields=["ip"]),
            models.Index(fields=["endpoint"]),
            models.Index(fields=["timestamp"]),
        ]
