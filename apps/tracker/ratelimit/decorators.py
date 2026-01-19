import hashlib
import secrets
import string

from functools import wraps
from datetime import timedelta, timezone, datetime

from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status

from core.models import Peer

from ratelimit.models import RateLimit

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

            count = RateLimit.objects.filter(
                Q(
                    peer=peer,
                    endpoint=endpoint,
                    timestamp__gte=timestamp,
                )
                |
                Q(
                    ip=ip,
                    endpoint=endpoint,
                    timestamp__gte=timestamp,
                )
            ).distinct().count()

            if count >= limit:
                return Response(
                    {
                        "limit": limit,
                        "per": per,
                        "key": endpoint,
                    }
                )

            else:
                RateLimit.objects.create(
                    id=hashlib.sha256(''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(64)).encode()).hexdigest(),
                    peer=peer,
                    ip=ip,
                    endpoint=endpoint,
                    timestamp=now,
                )


            return view_func(request, *args, **kwargs)

        return wrapped

    return decorator
