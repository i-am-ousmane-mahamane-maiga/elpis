from django.db import models
from django.db.models import ManyToManyField


class BaseModel(models.Model):
    id = models.CharField(primary_key=True, editable=False, unique=True, max_length=64)

    class Meta:
        abstract = True


class Song(BaseModel):
    class Meta:
        db_table = 'songs'

        indexes = [
            models.Index(fields=["id"]),
        ]


class Lyric(BaseModel):
    class Meta:
        db_table = 'lyrics'

        indexes = [
            models.Index(fields=["id"]),
        ]


class Album(BaseModel):
    class Meta:
        db_table = 'albums'

        indexes = [
            models.Index(fields=["id"]),
        ]


class Artist(BaseModel):
    class Meta:
        db_table = 'artists'

        indexes = [
            models.Index(fields=["id"]),
        ]


class Playlist(BaseModel):
    class Meta:
        db_table = 'playlists'

        indexes = [
            models.Index(fields=["id"]),
        ]


class Genre(BaseModel):
    class Meta:
        db_table = 'genres'

        indexes = [
            models.Index(fields=["id"]),
        ]


class Peer(BaseModel):
    ip = models.GenericIPAddressField()
    port = models.PositiveIntegerField()
    songs = models.ManyToManyField("Song", related_name="peers")
    albums = models.ManyToManyField("Album", related_name="peers")
    artists = models.ManyToManyField("Artist", related_name="peers")
    playlists = models.ManyToManyField("Playlist", related_name="peers")
    last_announce_timestamp = models.IntegerField()

    class Meta:
        db_table = 'peers'

        indexes = [
            models.Index(fields=["id"]),
        ]
