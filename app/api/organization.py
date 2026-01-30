from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.deps import get_session
from app.models.organization import Organization
from app.schemas.organization import OrganizationRead


router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.get("/{org_id}", response_model=OrganizationRead)
async def get_organization(
    org_id: int,
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(Organization)
        .options(selectinload(Organization.building))
        .options(selectinload(Organization.activities))
        .options(selectinload(Organization.phones))
        .where(Organization.id == org_id)
    )
    organization = result.scalars().first()
    if organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization


@router.get("/search", response_model=list[OrganizationRead])
async def search_organizations(
    name: str = Query(..., min_length=1),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(Organization)
        .options(selectinload(Organization.building))
        .options(selectinload(Organization.activities))
        .options(selectinload(Organization.phones))
        .where(Organization.name.ilike(f"%{name}%"))
    )
    return result.scalars().all()
