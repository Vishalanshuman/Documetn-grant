
from typing import AsyncGenerator
from app.config.db import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        # do something with the session if needed
        yield session


