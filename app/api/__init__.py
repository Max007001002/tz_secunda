from app.api.activity import router as activity_router
from app.api.building import router as building_router
from app.api.organization import router as organization_router

__all__ = ["activity_router", "building_router", "organization_router"]
