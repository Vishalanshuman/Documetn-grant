import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
)
from sqlalchemy.orm import sessionmaker

from main import app
from app.config.db import Base, get_db
from app.models.user import User
from app.models.document import Document

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

    async with TestingSessionLocal() as session:

        users = [
            User(name="Alice", id="11111111-1111-1111-1111-111111111111"),
            User(name="Bob", id="22222222-2222-2222-2222-222222222222"),
            User(name="Charlie", id="33333333-3333-3333-3333-333333333333"),
        ]

        documents = [
            Document(name="Document-1", id="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
            Document(name="Document-2", id="bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"),
            Document(name="Document-3", id="cccccccc-cccc-cccc-cccc-cccccccccccc"),
        ]

        session.add_all(users + documents)
        await session.commit()

        # 👇 Return the session to the test
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


from httpx import AsyncClient, ASGITransport

@pytest_asyncio.fixture
async def client(test_db):
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client