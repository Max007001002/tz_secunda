from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.activity import Activity


async def collect_descendant_ids(
    session: AsyncSession,
    root_ids: set[int],
) -> set[int]:
    ids = set(root_ids)
    level_ids = set(root_ids)

    for _ in range(3):
        if not level_ids:
            break
        result = await session.execute(
            select(Activity.id).where(Activity.parent_id.in_(level_ids))
        )
        child_ids = {row[0] for row in result.all()}
        new_ids = child_ids - ids
        if not new_ids:
            break
        ids |= new_ids
        level_ids = new_ids

    return ids
