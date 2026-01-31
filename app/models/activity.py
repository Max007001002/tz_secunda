from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.models.organization import organization_activity


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("activities.id"), nullable=True)

    parent: Mapped[Optional["Activity"]] = relationship(
        "Activity",
        remote_side=[id],
        backref="children",
    )
    organizations: Mapped[list["Organization"]] = relationship(
        "Organization",
        secondary=organization_activity,
        back_populates="activities",
    )
