
import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta
import uuid

from app.models.document import Document
from app.models.grant import GrantPermission
from app.models.user import User

pytestmark = pytest.mark.asyncio


async def test_create_grant(client: AsyncClient, test_db):
    # Seed data
    user_id = "11111111-1111-1111-1111-111111111111"
    doc_id = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"


    response = await client.post(
        "/api/v1/grants",
        params={"creator_id": str(user_id)},
        json={
            "grantee_id": str(user_id),
            "document_id": str(doc_id),
            "permission": "view",
            "expires_at": (datetime.utcnow() + timedelta(days=1)).isoformat(),
        },
    )
    print("Response------------>", response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["grantee_id"] == str(user_id)
    assert data["document_id"] == str(doc_id)
    assert data["permission"] == "view"
    assert not data["revoked"]
