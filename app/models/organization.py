from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


organization_activity = Table(
    "organization_activity",
    Base.metadata,
    Column("organization_id", ForeignKey("organizations.id"), primary_key=True),
    Column("activity_id", ForeignKey("activities.id"), primary_key=True),
)


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"), nullable=False)

    building: Mapped["Building"] = relationship(
        "Building",
        back_populates="organizations",
    )
    activities: Mapped[list["Activity"]] = relationship(
        "Activity",
        secondary=organization_activity,
        back_populates="organizations",
    )
    phones: Mapped[list["PhoneNumber"]] = relationship(
        "PhoneNumber",
        back_populates="organization",
        cascade="all, delete-orphan",
    )


class PhoneNumber(Base):
    __tablename__ = "organization_phones"

    id: Mapped[int] = mapped_column(primary_key=True)
    phone: Mapped[str] = mapped_column(String, nullable=False)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)

    organization: Mapped["Organization"] = relationship(
        "Organization",
        back_populates="phones",
    )
