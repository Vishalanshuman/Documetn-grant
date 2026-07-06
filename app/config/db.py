
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()


def get_database_url() -> str:
    url = os.getenv("DATABASE_URL", "").strip()
    if url:
        return url.strip('"').strip("'")
    return "postgresql+asyncpg://postgres:root@db:5432/grants_svc"


DATABASE_URL = get_database_url()
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
Base = declarative_base()


async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
