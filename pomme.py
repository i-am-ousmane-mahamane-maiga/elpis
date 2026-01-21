from apps.peer.database.db import init_db

release = {
    "artworks": [".data/storage/artworks/{variable}.ext"],
    "name": None,
    "description": None,
    "songs": ["id", ...],
    "artists": ["id", ...],
    "genres": ["id", ...],
}

song = {
    "artworks": [".data/storage/artworks/{variable}.ext"],
    "name": None,
    "description": None,
    "releases": ["id", ...],
    "artists": ["id", ...],
    "genres": ["id", ...],
    "file": ".data/storage/songs/id.mp3"
}

artist = {
    "artworks": [".data/storage/artworks/{variable}.ext"],
    "name": None,
    "description": None,
    "songs": ["id", ...],
    "releases": ["id", ...],
    "genres": ["id", ...],
}

playlist = {
    "artworks": [".data/storage/artworks/{variable}.ext"],
    "name": None,
    "description": None,
    "songs": ["id", ...],
}

genre = {
    "artworks": [".data/storage/artworks/{variable}.ext"],
    "name": None,
    "description": None,
    "songs": ["id", ...],
    "artists": ["id", ...],
    "genres": ["id", ...],
}

import asyncio

async def main():
    await init_db()
    print("Tracker DB ready")

asyncio.run(main())
