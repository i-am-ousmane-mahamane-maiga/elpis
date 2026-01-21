from apps.peer.database.db import init_db



import asyncio

async def main():
    await init_db()
    print("Tracker DB ready")

asyncio.run(main())
