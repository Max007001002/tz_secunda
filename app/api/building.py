from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.security import API_KEY_HEADER
from app.db.deps import get_session
from app.models.building import Building
from app.models.organization import Organization
from app.schemas.building import BuildingRead
from app.schemas.organization import OrganizationRead


router = APIRouter(
    prefix="/buildings",
    tags=["Buildings"],
    dependencies=[Security(API_KEY_HEADER)],
)


@router.get(
    "",
    response_model=list[BuildingRead],
    summary="Список зданий",
    description="Возвращает список всех зданий. Требуется заголовок X-API-Key.",
)
async def list_buildings(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Building))
    return result.scalars().all()


@router.get(
    "/{building_id}/organizations",
    response_model=list[OrganizationRead],
    summary="Организации в здании",
    description=(
        "Возвращает организации, находящиеся в указанном здании. "
        "Требуется заголовок X-API-Key."
    ),
)
async def organizations_in_building(
    building_id: int,
    session: AsyncSession = Depends(get_session),
):
    building = await session.get(Building, building_id)
    if building is None:
        raise HTTPException(status_code=404, detail="Building not found")

    result = await session.execute(
        select(Organization)
        .options(selectinload(Organization.building))
        .options(selectinload(Organization.activities))
        .options(selectinload(Organization.phones))
        .where(Organization.building_id == building_id)
    )
    return result.scalars().all()
