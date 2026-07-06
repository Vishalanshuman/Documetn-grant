# app/db/seed.py

from uuid import UUID

from sqlalchemy import select

from app.config.db import SessionLocal as AsyncSessionLocal
from app.models.user import User
from app.models.document import Document

# -------------------------
# Deterministic UUIDs
# -------------------------
ALICE_ID = UUID("11111111-1111-1111-1111-111111111111")
BOB_ID = UUID("22222222-2222-2222-2222-222222222222")
CAROL_ID = UUID("33333333-3333-3333-3333-333333333333")

Q1_REPORT_ID = UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
ROADMAP_ID = UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")
BUDGET_ID = UUID("cccccccc-cccc-cccc-cccc-cccccccccccc")


async def seed_users(session):
    users = [
        User(
            id=ALICE_ID,
            name="Alice",
        ),
        User(
            id=BOB_ID,
            name="Bob",
        ),
        User(
            id=CAROL_ID,
            name="Carol",
        ),
    ]

    for user in users:
        exists = await session.scalar(
            select(User).where(User.id == user.id)
        )

        if not exists:
            session.add(user)


async def seed_documents(session):
    documents = [
        Document(
            id=Q1_REPORT_ID,
            name="Q1 Report",
        ),
        Document(
            id=ROADMAP_ID,
            name="Product Roadmap",
        ),
        Document(
            id=BUDGET_ID,
            name="Budget 2026",
        ),
    ]

    for document in documents:
        exists = await session.scalar(
            select(Document).where(Document.id == document.id)
        )

        if not exists:
            session.add(document)


async def seed_database():
    async with AsyncSessionLocal() as session:

        await seed_users(session)
        await seed_documents(session)

        await session.commit()

        print("✅ Database seeded successfully.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(seed_database())