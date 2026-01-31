from math import asin, cos, radians, sin, sqrt

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.activity import collect_descendant_ids
from app.db.deps import get_session
from app.models.activity import Activity
from app.models.building import Building
from app.models.organization import Organization
from app.models.organization import organization_activity
from app.schemas.organization import OrganizationRead


router = APIRouter(prefix="/organizations", tags=["Organizations"])


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return radius * c


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


@router.get("/nearby", response_model=list[OrganizationRead])
async def organizations_nearby(
    lat: float = Query(...),
    lon: float = Query(...),
    radius: float = Query(..., gt=0),
    session: AsyncSession = Depends(get_session),
):
    delta_lat = radius / 111.0
    cos_lat = cos(radians(lat)) or 1e-6
    delta_lon = radius / (111.0 * cos_lat)
    lat_min = lat - delta_lat
    lat_max = lat + delta_lat
    lon_min = lon - delta_lon
    lon_max = lon + delta_lon

    result = await session.execute(
        select(Building).where(
            Building.latitude.between(lat_min, lat_max),
            Building.longitude.between(lon_min, lon_max),
        )
    )
    buildings = result.scalars().all()
    if not buildings:
        return []

    near_buildings = [
        building
        for building in buildings
        if _haversine_km(lat, lon, building.latitude, building.longitude) <= radius
    ]
    building_ids = [building.id for building in near_buildings]
    if not building_ids:
        return []

    result = await session.execute(
        select(Organization)
        .options(selectinload(Organization.building))
        .options(selectinload(Organization.activities))
        .options(selectinload(Organization.phones))
        .where(Organization.building_id.in_(building_ids))
    )
    return result.scalars().all()


@router.get("/within", response_model=list[OrganizationRead])
async def organizations_within(
    lat_min: float = Query(...),
    lat_max: float = Query(...),
    lon_min: float = Query(...),
    lon_max: float = Query(...),
    session: AsyncSession = Depends(get_session),
):
    if lat_min >= lat_max or lon_min >= lon_max:
        raise HTTPException(status_code=400, detail="Invalid bounding box")

    result = await session.execute(
        select(Building).where(
            Building.latitude.between(lat_min, lat_max),
            Building.longitude.between(lon_min, lon_max),
        )
    )
    buildings = result.scalars().all()
    if not buildings:
        return []

    building_ids = [building.id for building in buildings]
    result = await session.execute(
        select(Organization)
        .options(selectinload(Organization.building))
        .options(selectinload(Organization.activities))
        .options(selectinload(Organization.phones))
        .where(Organization.building_id.in_(building_ids))
    )
    return result.scalars().all()


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
