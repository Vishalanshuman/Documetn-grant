
import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta
import uuid

from app.models.document import Document
from app.models.grant import GrantPermission
from app.models.user import User

pytestmark = pytest.mark.asyncio


async def test_create_grant(client: AsyncClient, db_session):
    # Seed data
    user_id = uuid.uuid4()
    doc_id = uuid.uuid4()
    data = {
        "creator_id": str(user_id),
        "grantee_id": str(user_id),
        "document_id": str(doc_id),
        "permission": GrantPermission.VIEW,
        "revoked": False,
    }


    assert data["grantee_id"] == str(user_id)
    assert data["document_id"] == str(doc_id)
    assert data["permission"] == "view"
    assert not data["revoked"]
