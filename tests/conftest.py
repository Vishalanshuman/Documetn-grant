import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
)
from sqlalchemy.orm import sessionmaker

from main import app
from app.config.db import Base
from app.api.dependencies import get_db

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:root@localhost/grants_svc_test"

engine = create_async_engine(TEST_DATABASE_URL, echo=True)

TestingSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
)


async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture
async def test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session(test_db):
    async with TestingSessionLocal() as session:
        yield session


from httpx import AsyncClient, ASGITransport

@pytest_asyncio.fixture
async def client(test_db):
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client