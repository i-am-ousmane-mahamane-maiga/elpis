# apps/ratelimit/decorators.py
from functools import wraps
from datetime import timedelta, timezone, datetime

from django.db import transaction
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status

from core.models import Peer

# from .models import Limit


WINDOWS = {
    "second": timedelta(seconds=1),
    "minute": timedelta(minutes=1),
    "hour": timedelta(hours=1),
    "day": timedelta(days=1),
}


def get_client_ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


def rate_limit(
    *,
    limit: int,
    per: str = "minute",
    key: str | None = None,
):
    """
    limit=10, per='minute'|'hour'|'day'|'second'
    """

    if per not in WINDOWS:
        raise ValueError(f"Invalid window: {per}")

    window_delta = WINDOWS[per]

    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            now = datetime.now(timezone.utc)
            timestamp = now - window_delta

            peer = Peer.objects.filter(id=request.data["peer_id"])
            peer = peer.first() if peer.exists() else None

            ip = get_client_ip(request)
            endpoint = key or request.resolver_match.view_name or request.path

            # todo: stopped here

            with transaction.atomic():
                try:
                    pass

                except Exception as e:
                    pass

            return view_func(request, *args, **kwargs)

        return wrapped

    return decorator
