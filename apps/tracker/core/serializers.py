import os
import re

from rest_framework import serializers


class AnnounceSerializer(serializers.Serializer):
    peer_id = serializers.CharField(max_length=64, min_length=64)
    ip = serializers.IPAddressField()
    port = serializers.IntegerField()
    events = serializers.ListSerializer(
        child=serializers.JSONField()
    )
    timestamp = serializers.IntegerField()

    def validate_events(self, value):
        value = value[:int(os.getenv("EVENTS_LIMIT"))]

        events = {
            "keys": {
                "truth": {"key", "action", "type", "id"},
                "candidate": set(
                    [
                        key
                        for event in value
                        for key in event
                    ]
                ),
            },
            "actions": {
                "truth": {"get", "add", "remove"},
                "candidate": None
            },
            "types": {
                "truth": {"song", "lyric", "album", "artist", "playlist", "genre"},
                "candidate": None
            },
        }

        for key in ["action", "type"]:
            events[f"{key}s"]["candidate"] = set(
                [
                    i[key]
                    for i in value
                ]
            )

        else:
            for key, event in events.items():
                if not event["candidate"].issubset(event["truth"]):
                    raise serializers.ValidationError(f"There is an issue with one of the {key}")

            else:
                if not all(
                    [
                        self.is_sha256(event["id"])
                        for event in value
                    ]
                ):
                    raise serializers.ValidationError(f"There is an issue with one of the ids")

        if len(value) != len(
            set(
                [
                    str(i["key"])
                    for i in value
                ]
            )
        ):
            raise serializers.ValidationError("Duplicated are not allowed in keys")

        return super().validate(value)


    def validate_peer_id(self, value):
        if not self.is_sha256(value):
            raise serializers.ValidationError(f"peer_id must in sha256 hexdigest format")

        else:
            return value


    def is_sha256(self, candidate: str) -> bool:
        return bool(re.fullmatch(r"[A-Fa-f0-9]{64}", candidate))