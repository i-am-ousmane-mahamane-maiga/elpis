from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "artist" (
    "id" VARCHAR(64) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMP,
    "is_active" INT NOT NULL DEFAULT 1,
    "name" VARCHAR(255),
    "description" TEXT
);
        CREATE TABLE IF NOT EXISTS "genre" (
    "id" VARCHAR(64) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMP,
    "is_active" INT NOT NULL DEFAULT 1,
    "name" VARCHAR(255),
    "description" TEXT
);
        CREATE TABLE IF NOT EXISTS "song" (
    "id" VARCHAR(64) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMP,
    "is_active" INT NOT NULL DEFAULT 1,
    "name" VARCHAR(255),
    "description" TEXT,
    "file_id" VARCHAR(64) NOT NULL REFERENCES "media" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "lyrics" (
    "id" VARCHAR(64) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMP,
    "is_active" INT NOT NULL DEFAULT 1,
    "song_id" VARCHAR(64) NOT NULL UNIQUE REFERENCES "song" ("id") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "media" (
    "id" VARCHAR(64) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMP,
    "is_active" INT NOT NULL DEFAULT 1,
    "name" VARCHAR(255),
    "description" TEXT,
    "uri" VARCHAR(255) NOT NULL UNIQUE,
    "type" VARCHAR(255) NOT NULL
);
        CREATE TABLE IF NOT EXISTS "playlist" (
    "id" VARCHAR(64) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMP,
    "is_active" INT NOT NULL DEFAULT 1,
    "name" VARCHAR(255),
    "description" TEXT
);
        CREATE TABLE IF NOT EXISTS "release" (
    "id" VARCHAR(64) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMP,
    "is_active" INT NOT NULL DEFAULT 1,
    "name" VARCHAR(255),
    "description" TEXT
);
        DROP TABLE IF EXISTS "peer";
        CREATE TABLE "artist_media" (
    "artist_id" VARCHAR(64) NOT NULL REFERENCES "artist" ("id") ON DELETE CASCADE,
    "media_id" VARCHAR(64) NOT NULL REFERENCES "media" ("id") ON DELETE CASCADE
);
        CREATE TABLE "genre_media" (
    "genre_id" VARCHAR(64) NOT NULL REFERENCES "genre" ("id") ON DELETE CASCADE,
    "media_id" VARCHAR(64) NOT NULL REFERENCES "media" ("id") ON DELETE CASCADE
);
        CREATE TABLE "playlist_media" (
    "playlist_id" VARCHAR(64) NOT NULL REFERENCES "playlist" ("id") ON DELETE CASCADE,
    "media_id" VARCHAR(64) NOT NULL REFERENCES "media" ("id") ON DELETE CASCADE
);
        CREATE TABLE "release_media" (
    "release_id" VARCHAR(64) NOT NULL REFERENCES "release" ("id") ON DELETE CASCADE,
    "media_id" VARCHAR(64) NOT NULL REFERENCES "media" ("id") ON DELETE CASCADE
);
        CREATE TABLE "song_media" (
    "song_id" VARCHAR(64) NOT NULL REFERENCES "song" ("id") ON DELETE CASCADE,
    "media_id" VARCHAR(64) NOT NULL REFERENCES "media" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "artist_media";
        DROP TABLE IF EXISTS "artist_song";
        DROP TABLE IF EXISTS "artist_genre";
        DROP TABLE IF EXISTS "release_artist";
        DROP TABLE IF EXISTS "artist";
        DROP TABLE IF EXISTS "lyrics";
        DROP TABLE IF EXISTS "playlist_media";
        DROP TABLE IF EXISTS "playlist_song";
        DROP TABLE IF EXISTS "playlist";
        DROP TABLE IF EXISTS "genre_media";
        DROP TABLE IF EXISTS "release_genre";
        DROP TABLE IF EXISTS "song_genre";
        DROP TABLE IF EXISTS "genre";
        DROP TABLE IF EXISTS "release_media";
        DROP TABLE IF EXISTS "song_media";
        DROP TABLE IF EXISTS "media";
        DROP TABLE IF EXISTS "release_song";
        DROP TABLE IF EXISTS "song";
        DROP TABLE IF EXISTS "release";"""


MODELS_STATE = (
    "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"
)
