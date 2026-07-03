
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_db
from app.models import grant
from app.schema.grant import Grant, GrantCreate
from app.models.grant import Grant as GrantModel, GrantPermission
from app.models.user import User as UserModel
from app.models.document import Document as DocumentModel
from datetime import datetime, timedelta, timezone
from sqlalchemy.future import select
from app.crud.grant import grant_crud
import uuid
from uuid import UUID

router = APIRouter()


from typing import List


def normalize_datetime(value: datetime | None) -> datetime | None:
    if value is None:
        return None

    if value.tzinfo is not None:
        return value.astimezone(timezone.utc).replace(tzinfo=None)

    return value

@router.get("/grants", response_model=list[Grant])
async def list_grants(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await grant_crud.get_multi_by_filters(
        db,
        filters=and_(
            or_(
                GrantModel.creator_id == user_id,
                GrantModel.grantee_id == user_id,
            ),
            GrantModel.permission.in_(
                [
                    GrantPermission.VIEW,
                    GrantPermission.EDIT,
                    GrantPermission.ADMIN,
                ]
                    ),
                ),
            )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="No grants found."
        )

    return result

@router.get("/grants/{grant_id}", response_model=Grant)
async def get_grant(grant_id: UUID, user_id: UUID, db: AsyncSession = Depends(get_db)):
    grant = await grant_crud.get(db, grant_id)
    if not grant:
        raise HTTPException(status_code=404, detail="Grant not found")
    if grant.grantee_id != user_id and grant.creator_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    if grant.revoked or normalize_datetime(grant.expires_at) < datetime.utcnow():
        raise HTTPException(status_code=404, detail="Grant not found")
    if grant.permission not in [GrantPermission.VIEW, GrantPermission.EDIT, GrantPermission.ADMIN]:
        raise HTTPException(status_code=400, detail="Invalid permission")
    return grant



@router.delete("/grants/{grant_id}", status_code=204)
async def revoke_grant(
    grant_id: UUID,
    db: AsyncSession = Depends(get_db),
    creator_id: UUID =None,  # Hardcoded for now, will be replaced with auth
):
    if not creator_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    grant = await grant_crud.get(db, grant_id)
    if not grant:
        raise HTTPException(status_code=404, detail="Grant not found")

    # Business rule: Only the creator can revoke a grant.
    if grant.creator_id != creator_id:
        raise HTTPException(
            status_code=403,
            detail="Only the creator can revoke the grant.",
        )

    # Business rule: Cannot revoke already-revoked or expired grants.
    if grant.revoked:
        raise HTTPException(status_code=400, detail="Grant is already revoked.")

    if normalize_datetime(grant.expires_at) < datetime.utcnow():
        grant.revoked = True
        await db.commit()
        raise HTTPException(status_code=400, detail="Grant has already expired.")

    grant.revoked = True
    await db.commit()



@router.get("/grants/{grant_id}/check", response_model=dict)
async def check_grant_status(grant_id: UUID, db: AsyncSession = Depends(get_db)):
    grant = await grant_crud.get(db, grant_id)
    if not grant:
        raise HTTPException(status_code=404, detail="Grant not found")

    is_active = not grant.revoked and normalize_datetime(grant.expires_at) > datetime.utcnow()
    return {"is_active": is_active}


@router.post("/grants", response_model=Grant)
async def create_grant(
    grant: GrantCreate,
    db: AsyncSession = Depends(get_db),
    creator_id: UUID = None,  # Hardcoded for now, will be replaced with auth
):
    if not creator_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    expires_at = normalize_datetime(grant.expires_at)

    # Business rule: Expiry must be at least 1 minute in the future.
    if expires_at < datetime.utcnow() + timedelta(minutes=1):
        raise HTTPException(
            status_code=400,
            detail="Expiry must be at least 1 minute in the future.",
        )

    # Check if grantee and document exist
    grantee = await db.get(UserModel, grant.grantee_id)
    if not grantee:
        raise HTTPException(status_code=404, detail="Grantee not found")

    document = await db.get(DocumentModel, grant.document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Business rule: Only one active grant per grantee/document pair.
    existing_grant = await db.execute(
        select(GrantModel).where(
            GrantModel.grantee_id == grant.grantee_id,
            GrantModel.document_id == grant.document_id,
            GrantModel.revoked == False,
            GrantModel.expires_at > datetime.utcnow(),
        )
    )
    if existing_grant.scalars().first():
        raise HTTPException(
            status_code=400,
            detail="An active grant for this grantee and document already exists.",
        )

    grant_data = grant.dict()
    grant_data["expires_at"] = expires_at

    db_grant = GrantModel(
        **grant_data,
        creator_id=creator_id,
    )
    db.add(db_grant)
    await db.commit()
    await db.refresh(db_grant)
    return db_grant
