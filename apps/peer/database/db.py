from tortoise import Tortoise

TORTOISE_ORM = {
    "connections": {
        "default": "sqlite://db.sqlite3",
    },
    "apps": {
        "models": {
            "models": ["models"],
            "default_connection": "default",
        }
    },
    "use_tz": True,
    "timezone": "UTC",
}

async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
