from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.activity import collect_descendant_ids
from app.db.deps import get_session
from app.models.activity import Activity
from app.models.organization import Organization, organization_activity
from app.schemas.organization import OrganizationRead


router = APIRouter(prefix="/activities", tags=["Activities"])


@router.get(
    "/{activity_id}/organizations",
    response_model=list[OrganizationRead],
    summary="Организации по виду деятельности",
    description=(
        "Возвращает организации по виду деятельности и его подвидам "
        "(до 3 уровней). Требуется заголовок X-API-Key."
    ),
)
async def organizations_by_activity(
    activity_id: int,
    session: AsyncSession = Depends(get_session),
):
    activity = await session.get(Activity, activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity_ids = await collect_descendant_ids(session, {activity_id})

    result = await session.execute(
        select(Organization)
        .join(organization_activity)
        .options(selectinload(Organization.building))
        .options(selectinload(Organization.activities))
        .options(selectinload(Organization.phones))
        .where(organization_activity.c.activity_id.in_(activity_ids))
    )
    return result.unique().scalars().all()
