import os
import traceback

from django.db import transaction
from django.apps import apps
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.serializers import AnnounceSerializer
from core.models import Peer

from ratelimit.decorators import rate_limit


# todo: add security
# todo: add rate_limit with ip address

@api_view(["POST"])
@rate_limit(limit=1, per="hour")
def announce(request):
    try:
        serializer = AnnounceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        peer_id = serializer.validated_data["peer_id"]
        ip = serializer.validated_data["ip"]
        port = serializer.validated_data["port"]
        events = serializer.validated_data["events"]
        timestamp = serializer.validated_data["timestamp"]

        with transaction.atomic():
            try:
                peer = Peer.objects.get(
                    id=peer_id,
                )

                peer.last_announce_timestamp = timestamp

            except Peer.DoesNotExist:
                peer = Peer.objects.create(
                    id=peer_id,
                    ip=ip,
                    port=port,
                    last_announce_timestamp=timestamp,
                )

            results = handle_announce_events(peer, events, timestamp)

        return Response(
            {
                "ok": True,
                "message": "Announce received successfully",
                "data": results,
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        print(traceback.format_exc())
        return Response(
            {
                "ok": True,
                "message": "An error occurred",
                "data": {
                    "error": str(e),
                    "traceback": traceback.format_exc(),
                },
            },
            status=status.HTTP_200_OK
        )


def handle_announce_events(peer, events, timestamp):
    results = []

    for event in events:
        model = apps.get_model("core", event["type"].capitalize())
        result = {
            "key": event["key"]
        }

        try:
            _object = model.objects.get(id=event["id"])

        except model.DoesNotExist:
            if event["action"] == "add":
                _object = model.objects.create(id=event["id"])

            else:
                _object = None

        if _object:
            attribute = getattr(peer, f"{event['type']}s")

            match event["action"]:
                case "add":
                    attribute.add(_object)
                    result |= {
                        "ok": True,
                        "data": None
                    }

                case "get":
                    filters = {
                        f"{event["type"]}s__id": event["id"],
                        "last_announce_timestamp__gte": timestamp - int(os.getenv("ANNOUNCE_INTERVAL")),
                    }

                    result |= {
                        "ok": True,
                        "data": list(Peer.objects.filter(
                            **filters
                        ).exclude(
                            id=peer.id,
                        ).order_by(
                            "last_announce_timestamp"
                        ).values(
                            "ip", "port"
                        )[:int(os.getenv("PEERS_LIMIT"))])
                    }

                case "remove":
                    attribute.remove(_object)
                    result |= {
                        "ok": True,
                        "data": None
                    }

                case _:
                    raise ValueError("Unknown event")

        else:
            result |= {
                "ok": False,
                "data": None
            }

        results.append(result)

    else:
        return results