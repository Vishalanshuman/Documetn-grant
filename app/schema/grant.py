
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from app.models.grant import GrantPermission


class GrantBase(BaseModel):
    grantee_id: UUID
    document_id: UUID
    permission: GrantPermission
    expires_at: datetime


class GrantCreate(GrantBase):
    pass

class GrantUpdate(BaseModel):
    grantee_id: UUID | None = None
    document_id: UUID | None = None
    permission: GrantPermission | None = None
    expires_at: datetime | None = None
    revoked: bool | None = None

    
class Grant(GrantBase):
    id: UUID
    creator_id: UUID
    revoked: bool

    class Config:
        orm_mode = True
