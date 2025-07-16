import asyncio
import app.models as models 
from app.db import init_db

async def run():
    await init_db()

if __name__ == "__main__":
    asyncio.run(run())
