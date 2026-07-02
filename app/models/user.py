
import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.config.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)

    grants_created = relationship(
        "Grant",
        back_populates="creator",
        primaryjoin="Grant.creator_id == User.id",
        foreign_keys="Grant.creator_id",
    )

    grants_received = relationship(
        "Grant",
        back_populates="grantee",
        primaryjoin="Grant.grantee_id == User.id",
        foreign_keys="Grant.grantee_id",
    )