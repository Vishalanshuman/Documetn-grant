
import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Boolean,
    Enum as SAEnum,
)
from sqlalchemy.orm import relationship, validates
from sqlalchemy.dialects.postgresql import UUID
from app.config.db import Base
import enum


class GrantPermission(str, enum.Enum):
    VIEW = "view"
    EDIT = "edit"
    ADMIN = "admin"


class Grant(Base):
    __tablename__ = "grants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    creator_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    grantee_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    permission = Column(SAEnum(GrantPermission), nullable=False)

    creator = relationship(
        "User",
        back_populates="grants_created",
        primaryjoin="Grant.creator_id == User.id",
        foreign_keys="Grant.creator_id",
    )

    grantee = relationship(
        "User",
        back_populates="grants_received",
        primaryjoin="Grant.grantee_id == User.id",
        foreign_keys="Grant.grantee_id",
    )

    document = relationship(
        "Document",
        back_populates="grants",
        primaryjoin="Grant.document_id == Document.id",
        foreign_keys="Grant.document_id",
    )

    @validates("expires_at")
    def validate_expires_at(self, key, value):
        if value is None:
            return value

        if value.tzinfo is not None:
            value = value.astimezone(timezone.utc).replace(tzinfo=None)

        if value <= datetime.utcnow():
            raise ValueError("expires_at must be in the future")

        return value
    
