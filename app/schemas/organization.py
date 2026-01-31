from pydantic import BaseModel, ConfigDict, field_validator

from app.schemas.activity import ActivityRead
from app.schemas.building import BuildingRead


class OrganizationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    building: BuildingRead
    activities: list[ActivityRead]
    phones: list[str]

    @field_validator("phones", mode="before")
    @classmethod
    def normalize_phones(cls, value):
        if isinstance(value, list):
            normalized = []
            for item in value:
                if isinstance(item, str):
                    normalized.append(item)
                elif isinstance(item, dict) and "phone" in item:
                    normalized.append(item["phone"])
                elif hasattr(item, "phone"):
                    normalized.append(item.phone)
                else:
                    normalized.append(str(item))
            return normalized
        return value
