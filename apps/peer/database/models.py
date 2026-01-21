from tortoise import fields, models


class BaseModel(models.Model):
    id = fields.CharField(pk=True, max_length=64)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    deleted_at = fields.DatetimeField(null=True)
    is_active = fields.BooleanField(default=True)

    class Meta:
        abstract = True


class Details(BaseModel):
    name = fields.CharField(max_length=255, null=True)
    description = fields.TextField(null=True)

    class Meta:
        abstract = True


class Media(Details):
    uri = fields.CharField(unique=True, max_length=255)
    type = fields.CharField(max_length=255)


class Release(Details):
    artworks = fields.ManyToManyField("models.Media", related_name="releases")
    songs = fields.ManyToManyField("models.Song", related_name="releases")
    artists = fields.ManyToManyField("models.Artist", related_name="releases")
    genres = fields.ManyToManyField("models.Genre", related_name="releases")


class Song(Details):
    artworks = fields.ManyToManyField("models.Media", related_name="songs")
    genres = fields.ManyToManyField("models.Genre", related_name="songs")
    file = fields.ForeignKeyField("models.Media", related_name="song_files", on_delete=fields.CASCADE)


class Artist(Details):
    artworks = fields.ManyToManyField("models.Media", related_name="artists")
    songs = fields.ManyToManyField("models.Song", related_name="artists")
    genres = fields.ManyToManyField("models.Genre", related_name="artists")


class Playlist(Details):
    artworks = fields.ManyToManyField("models.Media", related_name="playlists")
    songs = fields.ManyToManyField("models.Song", related_name="playlists")


class Lyrics(BaseModel):
    song = fields.OneToOneField("models.Song", related_name="lyrics", on_delete=fields.CASCADE)


class Genre(Details):
    artworks = fields.ManyToManyField("models.Media", related_name="genres")
