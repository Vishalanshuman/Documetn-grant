
import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta
import uuid

from app.models.grant import GrantPermission

pytestmark = pytest.mark.anyio


async def test_create_grant(client: AsyncClient):
    # Seed data
    user_id = uuid.uuid4()
    doc_id = uuid.uuid4()

    response = await client.post(
        "/api/v1/grants",
        json={
            "grantee_id": str(user_id),
            "document_id": str(doc_id),
            "permission": "view",
            "expires_at": (datetime.utcnow() + timedelta(days=1)).isoformat(),
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["grantee_id"] == str(user_id)
    assert data["document_id"] == str(doc_id)
    assert data["permission"] == "view"
    assert not data["revoked"]
