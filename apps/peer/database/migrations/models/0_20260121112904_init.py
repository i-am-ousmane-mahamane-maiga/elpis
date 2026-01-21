from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "peer" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "peer_id" VARCHAR(64) NOT NULL UNIQUE,
    "secret_hash" VARCHAR(64) NOT NULL,
    "port" INT NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztll1v2jAUhv9KlCsmdVWbUVrtLmVMZRpQtdmHWlWRSUwS4dip7axFFf99Pk6CQwoMpE"
    "oFaXfJe17H5zyxffxipyzERBxfY8ztz9aLTVGK1cOSfmTZKMuMCoJEY6KNWeUYC8lRIJU2"
    "QURgJYVYBDzJZMKoUmlOCIgsUMaERkbKafKYY1+yCMtY53H/oOSEhvgZi+o1m/qTBJNwKc"
    "0khLm17stZprU+lV+1EWYb+wEjeUqNOZvJmNGFO6ES1AhTzJHE8HnJc0gfsiurrCoqMjWW"
    "IsXamBBPUE5krdwtGQSMAj+VjdAFRjDLR+e0fd6++NRpXyiLzmShnM+L8kztxUBNYOjZcx"
    "1HEhUOjdFwg7/mr4LXjRFfTa82pIFQJd5EWAF7V4YpevYJppGM1WunvQHYT/eme+XetDrt"
    "D1AJUwu5WN3DMuLoEDA1DAUOOJZ+jES8C8fGsLdhWQkGptmEh0EzY1zusJcr+793857ge5"
    "MNbXCpNQT1+WgFtC8qIpMUrya3PLLBLyyHHlcPe0pT1RCOKJmVp8YGdF5/0Lv13ME1VJIK"
    "8Ug0ItfrQcTR6qyhtjqNhbv4iPWr711Z8GrdjYY9TZAJGXE9o/F5dzbkhHLJfMqefBTWDr"
    "hKrcDMob1NprWDGoQxCqZPiIf+qwhz2Drv61DqpE0FURTp3wJwIc2y2buYJ0G86hpQRjZe"
    "BJDx/L8K7N3Jsf4q8AdzASnt0MJqQw6zfTlnZ1v0L+Va28B0bPlIhq2xA8TSfpgAT09Otg"
    "CoXGsB6lijpzEqMV3R0L7djoZrmpkZ0gD5g6oC78MkkEcWSYR82E+sGyhC1UtNq4LXGri/"
    "m1y730eXzW4EH7hUjN+1vcz/AgOulJ8="
)
