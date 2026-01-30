"""Тестовые данные.

Revision ID: 0002_seed_data
Revises: 0001_create_tables
Create Date: 2026-01-30
"""

from alembic import op
import sqlalchemy as sa


revision = "0002_seed_data"
down_revision = "0001_create_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    buildings_table = sa.table(
        "buildings",
        sa.column("id", sa.Integer),
        sa.column("address", sa.String),
        sa.column("latitude", sa.Float),
        sa.column("longitude", sa.Float),
    )

    activities_table = sa.table(
        "activities",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
        sa.column("parent_id", sa.Integer),
    )

    organizations_table = sa.table(
        "organizations",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
        sa.column("building_id", sa.Integer),
    )

    phones_table = sa.table(
        "organization_phones",
        sa.column("id", sa.Integer),
        sa.column("phone", sa.String),
        sa.column("organization_id", sa.Integer),
    )

    org_activity_table = sa.table(
        "organization_activity",
        sa.column("organization_id", sa.Integer),
        sa.column("activity_id", sa.Integer),
    )

    op.bulk_insert(
        buildings_table,
        [
            {
                "id": 1,
                "address": "г. Москва, ул. Ленина 1, офис 3",
                "latitude": 55.7558,
                "longitude": 37.6176,
            },
            {
                "id": 2,
                "address": "г. Москва, ул. Блюхера 32/1",
                "latitude": 55.7601,
                "longitude": 37.65,
            },
            {
                "id": 3,
                "address": "г. Санкт-Петербург, Невский пр. 10",
                "latitude": 59.9343,
                "longitude": 30.3351,
            },
        ],
    )

    op.bulk_insert(
        activities_table,
        [
            {"id": 1, "name": "Еда", "parent_id": None},
            {"id": 2, "name": "Мясная продукция", "parent_id": 1},
            {"id": 3, "name": "Молочная продукция", "parent_id": 1},
            {"id": 4, "name": "Автомобили", "parent_id": None},
            {"id": 5, "name": "Легковые", "parent_id": 4},
            {"id": 6, "name": "Грузовые", "parent_id": 4},
            {"id": 7, "name": "Запчасти", "parent_id": 4},
            {"id": 8, "name": "Аксессуары", "parent_id": 7},
            {"id": 9, "name": "IT", "parent_id": None},
            {"id": 10, "name": "Разработка ПО", "parent_id": 9},
            {"id": 11, "name": "Веб-разработка", "parent_id": 10},
        ],
    )

    op.bulk_insert(
        organizations_table,
        [
            {"id": 1, "name": "ООО Рога и Копыта", "building_id": 2},
            {"id": 2, "name": "Молочные продукты", "building_id": 1},
            {"id": 3, "name": "Грузовик-Сервис", "building_id": 2},
            {"id": 4, "name": "АвтоЗапчасть+", "building_id": 3},
            {"id": 5, "name": "ИТ Центр", "building_id": 1},
            {"id": 6, "name": "Мясной двор", "building_id": 1},
        ],
    )

    op.bulk_insert(
        phones_table,
        [
            {"id": 1, "phone": "2-222-222", "organization_id": 1},
            {"id": 2, "phone": "3-333-333", "organization_id": 1},
            {"id": 3, "phone": "8-923-666-13-13", "organization_id": 1},
            {"id": 4, "phone": "8-800-555-35-35", "organization_id": 2},
            {"id": 5, "phone": "+7-495-123-45-67", "organization_id": 5},
            {"id": 6, "phone": "+7-812-000-00-00", "organization_id": 4},
            {"id": 7, "phone": "+7-495-765-43-21", "organization_id": 5},
            {"id": 8, "phone": "+7-495-111-11-11", "organization_id": 6},
        ],
    )

    op.bulk_insert(
        org_activity_table,
        [
            {"organization_id": 1, "activity_id": 2},
            {"organization_id": 1, "activity_id": 3},
            {"organization_id": 2, "activity_id": 3},
            {"organization_id": 3, "activity_id": 6},
            {"organization_id": 4, "activity_id": 7},
            {"organization_id": 4, "activity_id": 8},
            {"organization_id": 5, "activity_id": 9},
            {"organization_id": 5, "activity_id": 10},
            {"organization_id": 5, "activity_id": 11},
            {"organization_id": 6, "activity_id": 2},
        ],
    )


def downgrade() -> None:
    op.execute("DELETE FROM organization_activity")
    op.execute("DELETE FROM organization_phones")
    op.execute("DELETE FROM organizations")
    op.execute("DELETE FROM activities")
    op.execute("DELETE FROM buildings")
