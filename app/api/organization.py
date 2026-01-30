from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.activity import collect_descendant_ids
from app.db.deps import get_session
from app.models.activity import Activity
from app.models.organization import Organization
from app.models.organization import organization_activity
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
    name: str | None = Query(None, min_length=1),
    activity: str | None = Query(None, min_length=1),
    session: AsyncSession = Depends(get_session),
):
    if name and activity:
        raise HTTPException(
            status_code=400, detail="Use either 'name' or 'activity' search"
        )
    if not name and not activity:
        raise HTTPException(
            status_code=400, detail="Either 'name' or 'activity' is required"
        )

    if name:
        result = await session.execute(
            select(Organization)
            .options(selectinload(Organization.building))
            .options(selectinload(Organization.activities))
            .options(selectinload(Organization.phones))
            .where(Organization.name.ilike(f"%{name}%"))
        )
        return result.scalars().all()

    result = await session.execute(
        select(Activity.id).where(Activity.name.ilike(f"%{activity}%"))
    )
    matched_ids = {row[0] for row in result.all()}
    if not matched_ids:
        return []

    activity_ids = await collect_descendant_ids(session, matched_ids)
    result = await session.execute(
        select(Organization)
        .join(organization_activity)
        .options(selectinload(Organization.building))
        .options(selectinload(Organization.activities))
        .options(selectinload(Organization.phones))
        .where(organization_activity.c.activity_id.in_(activity_ids))
    )
    return result.unique().scalars().all()
