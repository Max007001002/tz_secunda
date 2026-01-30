from pydantic import BaseModel, ConfigDict

from app.schemas.activity import ActivityRead
from app.schemas.building import BuildingRead


class PhoneNumberRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    phone: str


class OrganizationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    building: BuildingRead
    activities: list[ActivityRead]
    phones: list[PhoneNumberRead]
